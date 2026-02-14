from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from typing import Optional, List, Dict, Any
from db import get_session
from services import chat_service, gemini_service
from services import tasks as task_service
from middleware.jwt import get_current_user

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]

def execute_tool(tool_name: str, args: Dict[str, Any], session: Session):
    """Execute tools"""
    user_id = args.get('user_id')

    if tool_name == "add_task":
        task = task_service.create_task(
            session,
            user_id,
            args['title'],
            args.get('description', '')
        )
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }

    elif tool_name == "list_tasks":
        tasks = task_service.get_tasks(
            session,
            user_id,
            args.get('status', 'all')
        )
        return {
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "completed": t.completed,
                    "created_at": str(t.created_at)
                }
                for t in tasks
            ]
        }

    elif tool_name == "complete_task":
        task = task_service.toggle_complete(
            session,
            user_id,
            args['task_id']
        )
        if not task:
            return {"error": "Task not found"}
        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }

    elif tool_name == "delete_task":
        success = task_service.delete_task(
            session,
            user_id,
            args['task_id']
        )
        if not success:
            return {"error": "Task not found"}
        return {
            "task_id": args['task_id'],
            "status": "deleted"
        }

    return {"error": "Unknown tool"}

@router.post("", response_model=ChatResponse)
def send_message(
    user_id: str,
    data: ChatRequest,
    session: Session = Depends(get_session),
    token_user_id: str = Depends(get_current_user)
):
    """Send a message to the AI chatbot"""
    # Validate that URL user_id matches token user_id
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You can only access your own conversations"
        )

    try:
        # Get or create conversation
        conversation = chat_service.get_or_create_conversation(
            session,
            user_id,
            data.conversation_id
        )

        # Load conversation history
        history = chat_service.load_conversation_history(
            session,
            conversation.id
        )

        # Save user message
        chat_service.save_message(
            session,
            conversation.id,
            user_id,
            "user",
            data.message
        )

        # Create tool executor
        def tool_executor(tool_name: str, args: Dict[str, Any]):
            return execute_tool(tool_name, args, session)

        # Get AI response
        result = gemini_service.chat_with_gemini(
            user_id,
            data.message,
            history,
            tool_executor
        )

        # Save AI response
        chat_service.save_message(
            session,
            conversation.id,
            user_id,
            "assistant",
            result["response"]
        )

        return ChatResponse(
            conversation_id=conversation.id,
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )

    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(500, f"Chat error: {str(e)}")