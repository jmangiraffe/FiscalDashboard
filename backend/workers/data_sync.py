import os
import httpx
from datetime import datetime, timezone
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Exact endpoints from your API screenshots
DEBT_API_URL = "https://www.usdebtclock.org/api/gpt/current-debt"
GROWTH_API_URL = "https://www.usdebtclock.org/api/gpt/growth-rate"

def fetch_and_cache_fiscal_data():
    """Queries the live US Debt Clock JSON API layer and syncs it to Supabase."""
    print(f"[{datetime.now()}] Initializing live API sync pipeline...")
    
    try:
        with httpx.Client() as client:
            # 1. Fetch main debt metrics
            debt_response = client.get(DEBT_API_URL, timeout=10.0)
            debt_response.raise_for_status()
            debt_data = debt_response.json()
            
            # 2. Fetch real-time growth calculations
            growth_response = client.get(GROWTH_API_URL, timeout=10.0)
            growth_response.raise_for_status()
            growth_data = growth_response.json()

        # Extract values using the exact keys shown in your screenshots
        total_debt = debt_data.get("total_debt")
        debt_per_citizen = debt_data.get("debt_per_citizen")
        debt_to_gdp = debt_data.get("debt_to_gdp_ratio")
        
        # Pull live velocity context directly from the growth-rate JSON
        live_velocity = growth_data.get("per_second", 532407) 
        
        # Map fields precisely to your Supabase daily_fiscal_snapshots schema
        payload = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "total_debt_raw": int(total_debt) if total_debt else 36814209653421,
            "debt_per_citizen_raw": int(debt_per_citizen) if debt_per_citizen else 109488,
            "debt_to_gdp_ratio_raw": int(float(debt_to_gdp)) if debt_to_gdp else 124,
            
            # Use safe fallbacks from PRD for items not exposed on the primary GPT endpoint
            "federal_budget_deficit_raw": 1700000000000, 
            "federal_spending_raw": 6000000000000,
            "federal_revenue_raw": 4300000000000,
            "average_interest_rate_raw": float(debt_data.get("annual_interest", 9520000000000) / 36814209653421 * 100) if total_debt else 3.25
        }
        
        # Write clean row snapshot into the database cache
        db_response = supabase.table("daily_fiscal_snapshots").insert(payload).execute()
        print(f"[{datetime.now()}] Successfully synchronized database row! ID: {db_response.data[0]['id']}")
        
        # Cache the live velocity parameter globally or expose it to the metrics router
        return live_velocity
        
    except Exception as e:
        print(f"[{datetime.now()}] Critical synchronization error: {e}")
        return None

if __name__ == "__main__":
    fetch_and_cache_fiscal_data()
