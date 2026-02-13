from sqlmodel import Session, select
from backend.models import Conversation, Message
from typing import List, Dict, Optional
from datetime import datetime

def get_or_create_conversation(
    session: Session,
    user_id: str,
    conversation_id: Optional[int] = None
) -> Conversation:
    """Get existing conversation or create new one"""
    if conversation_id:
        conv = session.get(Conversation, conversation_id)
        if conv and conv.user_id == user_id:
            return conv
    
    # Create new conversation
    conv = Conversation(user_id=user_id)
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv

def load_conversation_history(
    session: Session,
    conversation_id: int
) -> List[Dict[str, str]]:
    """Load all messages from a conversation"""
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()
    
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]

def save_message(
    session: Session,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str
) -> Message:
    """Save a message to the conversation"""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message