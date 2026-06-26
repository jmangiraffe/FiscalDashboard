import os
import httpx
from datetime import datetime, timezone
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Missing required environment variables: SUPABASE_URL and SUPABASE_KEY must be set. "
        "Copy .env.example to .env and fill in your Supabase credentials."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

CURRENT_DEBT_URL = "https://www.us-debt-clock.com/api/gpt/current-debt"
GROWTH_RATE_URL = "https://www.us-debt-clock.com/api/gpt/growth-rate"

# Reasonable fallback constants (used only when API is unavailable)
_FALLBACK_TOTAL_DEBT = 36_814_209_653_421
_FALLBACK_ANNUAL_INTEREST = 952_000_000_000

def fetch_and_cache_fiscal_data():
    """Queries the external US Debt Clock JSON API and caches a clean snapshot in Supabase."""
    print(f"[{datetime.now()}] Starting fiscal data sync...")

    try:
        with httpx.Client() as client:
            debt_res = client.get(CURRENT_DEBT_URL, timeout=10.0)
            debt_res.raise_for_status()
            debt_data = debt_res.json()

            growth_res = client.get(GROWTH_RATE_URL, timeout=10.0)
            growth_res.raise_for_status()
            growth_data = growth_res.json()

        total_debt = int(debt_data.get("total_debt") or _FALLBACK_TOTAL_DEBT)
        annual_interest = float(debt_data.get("annual_interest") or _FALLBACK_ANNUAL_INTEREST)

        # Guard against division by zero
        if total_debt == 0:
            raise ValueError("total_debt is zero — cannot compute interest rate ratio.")

        payload = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "total_debt_raw": total_debt,
            "debt_per_citizen_raw": int(debt_data.get("debt_per_citizen") or 109_488),
            "debt_to_gdp_ratio_raw": float(debt_data.get("debt_to_gdp_ratio") or 124.3),
            "federal_budget_deficit_raw": int(growth_data.get("annual_increase") or 1_680_000_000_000),
            "federal_spending_raw": 6_000_000_000_000,
            "federal_revenue_raw": 4_300_000_000_000,
            "average_interest_rate_raw": round((annual_interest / total_debt) * 100, 4),
        }

        db_response = supabase.table("daily_fiscal_snapshots").insert(payload).execute()
        print(f"[{datetime.now()}] Sync successful. Row ID: {db_response.data[0]['id']}")

    except httpx.HTTPStatusError as e:
        print(f"[{datetime.now()}] External API error ({e.response.status_code}): {e}")
    except httpx.RequestError as e:
        print(f"[{datetime.now()}] Network error reaching external API: {e}")
    except Exception as e:
        print(f"[{datetime.now()}] Data sync failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    fetch_and_cache_fiscal_data()
