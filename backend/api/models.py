from pydantic import BaseModel, Field
from typing import Optional, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    session_id: str = Field(..., description="Session ID for this conversation")
    intent: Optional[str] = Field(None, description="Classified intent of the message")
    response: str = Field(..., description="AI response text")
    context_data: Optional[Any] = Field(None, description="Additional context data based on intent")
    timestamp: str = Field(..., description="Response timestamp")


class NewSessionResponse(BaseModel):
    """Response model for new session creation"""
    session_id: str = Field(..., description="New session ID")
    message: str = Field(..., description="Success message")


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")