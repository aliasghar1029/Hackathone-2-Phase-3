# [Task]: T-015
# [From]: speckit.plan §3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from ..db import get_session
from ..services import chat
from ..middleware.jwt import verify_user_id
from typing import Optional, List

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict]

@router.post("", response_model=ChatResponse)
def send_message(
    user_id: str,
    data: ChatRequest,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    try:
        # Get or create conversation
        conversation = chat.get_or_create_conversation(session, user_id, data.conversation_id)

        # Load history
        history = chat.load_history(session, conversation.id)

        # Save user message
        chat.save_message(session, conversation.id, user_id, "user", data.message)

        # Build message array
        messages = history + [{"role": "user", "content": data.message}]

        # Run agent
        result = chat.run_agent(user_id, messages)

        # Save assistant response
        chat.save_message(session, conversation.id, user_id, "assistant", result["response"])

        return {
            "conversation_id": conversation.id,
            "response": result["response"],
            "tool_calls": result["tool_calls"]
        }

    except Exception as e:
        raise HTTPException(500, f"Chat error: {str(e)}")