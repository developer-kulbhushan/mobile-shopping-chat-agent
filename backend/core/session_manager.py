from datetime import datetime, timedelta
from typing import Dict, Optional
from threading import Lock
import uuid


class SessionManager:
    """Thread-safe session manager for handling chat sessions"""
    
    def __init__(self, timeout: int = 3600):
        self._sessions: Dict[str, Dict] = {}
        self._lock = Lock()
        self.timeout = timeout
    
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        with self._lock:
            self._sessions[session_id] = {
                "created_at": datetime.now(),
                "last_accessed": datetime.now(),
                "messages": []
            }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data by session ID"""
        with self._lock:
            if session_id not in self._sessions:
                return None
            
            session = self._sessions[session_id]
            
            # Check if session has expired
            if datetime.now() - session["last_accessed"] > timedelta(seconds=self.timeout):
                del self._sessions[session_id]
                return None
            
            session["last_accessed"] = datetime.now()
            return session
    
    def update_session(self, session_id: str, messages: list):
        """Update session with new messages"""
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id]["messages"] = messages
                self._sessions[session_id]["last_accessed"] = datetime.now()
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        with self._lock:
            current_time = datetime.now()
            expired = [
                sid for sid, data in self._sessions.items()
                if current_time - data["last_accessed"] > timedelta(seconds=self.timeout)
            ]
            for sid in expired:
                del self._sessions[sid]


# Global session manager instance
session_manager = SessionManager()