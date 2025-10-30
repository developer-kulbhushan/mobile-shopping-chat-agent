import logging
from supabase import create_client, Client
from core.config import settings

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """Initializes and returns the Supabase client."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def create_logs_table_if_not_exists():
    """
    Connects to Supabase and creates the 'logs' table by calling a SQL function.
    """
    try:
        supabase = get_supabase_client()

        # Call the RPC function in Supabase to create the table
        supabase.rpc('create_logs_table').execute()
        logger.info("Successfully ensured 'logs' table exists.")

    except Exception as e:
        # A more robust check might be needed if the rpc call fails for reasons other than the table existing
        logger.warning(f"Could not ensure 'logs' table exists, it might already be there. Error: {e}")

if __name__ == "__main__":
    create_logs_table_if_not_exists()
