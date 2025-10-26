from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging

from api.models import ChatRequest, ChatResponse, NewSessionResponse, ErrorResponse
from core.session_manager import session_manager
from agent.graph import process_message

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response
    
    - **message**: User's message text
    - **session_id**: Optional session ID for conversation continuity
    """
    try:
        # Create new session if not provided
        if not request.session_id:
            session_id = session_manager.create_session()
            logger.info(f"Created new session: {session_id}")
        else:
            session_id = request.session_id
            session = session_manager.get_session(session_id)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Session not found or expired. Please create a new session."
                )
        
        # Get session data
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Process the message through the agent
        result = await process_message(
            message=request.message,
            conversation_history=session["messages"]
        )
        
        # Update session with new messages
        session_manager.update_session(session_id, result["messages"])
        
        logger.info(f"Processed message for session {session_id}, intent: {result.get('intent')}")
        
        return ChatResponse(
            session_id=session_id,
            intent=result.get("intent"),
            response=result.get("response", ""),
            context_data=result.get("context_data"),
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your message. Please try again."
        )


@router.post(
    "/sessions/new",
    response_model=NewSessionResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_new_session():
    """Create a new chat session"""
    try:
        session_id = session_manager.create_session()
        logger.info(f"Created new session via endpoint: {session_id}")
        return NewSessionResponse(
            session_id=session_id,
            message="New session created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating session: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating session"
        )


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_session(session_id: str):
    """Delete a chat session"""
    try:
        session_manager.delete_session(session_id)
        logger.info(f"Deleted session: {session_id}")
        return None
    except Exception as e:
        logger.error(f"Error deleting session: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting session"
        )


@router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or expired"
            )
        
        return {
            "session_id": session_id,
            "messages": session["messages"],
            "created_at": session["created_at"].isoformat(),
            "last_accessed": session["last_accessed"].isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving session history"
        )
