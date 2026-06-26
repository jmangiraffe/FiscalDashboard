import os
import httpx
from datetime import datetime, timezone
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Exact API Endpoints from documentation
CURRENT_DEBT_URL = "https://www.us-debt-clock.com/api/gpt/current-debt"
GROWTH_RATE_URL = "https://www.us-debt-clock.com/api/gpt/growth-rate"

def fetch_and_cache_fiscal_data():
    """Queries the external US Debt Clock JSON API and caches a clean snapshot in Supabase."""
    print(f"[{datetime.now()}] Initializing background API synchronization data task...")
    
    try:
        with httpx.Client() as client:
            # 1. Fetch current metrics
            debt_res = client.get(CURRENT_DEBT_URL, timeout=10.0)
            debt_res.raise_for_status()
            debt_data = debt_res.json()
            
            # 2. Fetch growth calculations
            growth_res = client.get(GROWTH_RATE_URL, timeout=10.0)
            growth_res.raise_for_status()
            growth_data = growth_res.json()

        # Build clean database payload following your exact table schema definitions
        payload = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "total_debt_raw": int(debt_data.get("total_debt", 36814209653421)),
            "debt_per_citizen_raw": int(debt_data.get("debt_per_citizen", 109488)),
            "debt_to_gdp_ratio_raw": int(float(debt_data.get("debt_to_gdp_ratio", 124.3))),
            
            # Fallbacks from PRD parameters for metrics not provided by these two endpoints
            "federal_budget_deficit_raw": int(growth_data.get("annual_increase", 1680000000000)),
            "federal_spending_raw": 6000000000000,
            "federal_revenue_raw": 4300000000000,
            "average_interest_rate_raw": float((debt_data.get("annual_interest", 952000000000) / debt_data.get("total_debt", 36814209653421)) * 100)
        }
        
        # Save snapshot into Supabase table
        db_response = supabase.table("daily_fiscal_snapshots").insert(payload).execute()
        print(f"[{datetime.now()}] Cache update successful! Row ID: {db_response.data[0]['id']}")
        
    except Exception as e:
        print(f"[{datetime.now()}] Data sync pipeline failed: {e}")

if __name__ == "__main__":
    fetch_and_cache_fiscal_data()
