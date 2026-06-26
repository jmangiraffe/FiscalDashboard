import os
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

def get_latest_snapshot():
    """Fetches the most recent cached fiscal snapshot from Supabase."""
    try:
        response = (
            supabase.table("daily_fiscal_snapshots")
            .select("*")
            .order("captured_at", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"[db_service] Database error: {e}")
        return None
