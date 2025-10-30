import logging
from typing import Dict, Any, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from core.supabase_client import get_supabase_client
from agent.models.log_entry import LogEntry

logger = logging.getLogger(__name__)
IST = ZoneInfo("Asia/Kolkata")

class LogService:
    """A service for logging chat session events to Supabase."""

    def __init__(self):
        self.supabase = get_supabase_client()

    def log_event(
        self,
        session_id: str,
        event_type: str,
        user_message: Optional[str] = None,
        bot_response: Optional[str] = None,
        intent: Optional[str] = None,
        error_details: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Logs an event to the Supabase 'logs' table after validating it
        against the LogEntry model and converting the timestamp to IST.
        """
        try:
            # Create a LogEntry instance to validate the data
            log_entry = LogEntry(
                session_id=session_id,
                event_type=event_type,
                timestamp=datetime.now(IST),
                user_message=user_message,
                bot_response=bot_response,
                intent=intent,
                error_details=error_details,
                metadata=metadata,
            )

            # Convert the Pydantic model to a dictionary for Supabase
            log_dict = log_entry.model_dump(exclude_none=True)

            self.supabase.table("logs").insert(log_dict).execute()
        except Exception as e:
            logger.error(f"Failed to log event to Supabase: {e}", exc_info=True)

# Global instance of the LogService
log_service = LogService()
