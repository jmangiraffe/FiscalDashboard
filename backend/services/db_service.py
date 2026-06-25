import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_latest_snapshot():
    """
    Fetches the most recent fiscal snapshot from Supabase.
    """
    try:
        # Query the table, order by captured_at descending, limit to 1
        response = supabase.table("daily_fiscal_snapshots").select("*").order("captured_at", desc=True).limit(1).execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Database Error: {e}")
        return None
