from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class LogEntry(BaseModel):
    """
    Pydantic model for a log entry, representing the schema of the 'logs' table.
    This model ensures that all log data is structured and validated before being
    sent to the database.
    """
    session_id: str
    event_type: str
    timestamp: datetime
    user_message: Optional[str] = None
    bot_response: Optional[str] = None
    intent: Optional[str] = None
    error_details: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        # This configuration allows the model to be created from class attributes
        # and helps with serialization to JSON, which is useful for sending
        # data to the database.
        from_attributes = True
