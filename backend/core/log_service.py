import logging
from typing import Dict, Any, Optional
from core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

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
        Logs an event to the Supabase 'logs' table.

        Args:
            session_id: The ID of the session.
            event_type: The type of event (e.g., 'new_session', 'message', 'error').
            user_message: The user's message.
            bot_response: The bot's response.
            intent: The classified intent of the message.
            error_details: Details of any error that occurred.
            metadata: Any other relevant data.
        """
        try:
            log_entry = {
                "session_id": session_id,
                "event_type": event_type,
                "user_message": user_message,
                "bot_response": bot_response,
                "intent": intent,
                "error_details": error_details,
                "metadata": metadata,
            }
            self.supabase.table("logs").insert(log_entry).execute()
        except Exception as e:
            logger.error(f"Failed to log event to Supabase: {e}", exc_info=True)

# Global instance of the LogService
log_service = LogService()
