# [Task]: T-013 & T-014
# [From]: speckit.plan §2.2 & §5

from sqlmodel import Session, select
from ..models import Conversation, Message
from typing import List, Optional
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
from backend.mcp.server import get_mcp_tools

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AGENT_INSTRUCTIONS = """
You are a helpful todo assistant. You help users manage their tasks through natural language.

When the user wants to:
- Add a task → Use add_task tool
- See tasks → Use list_tasks tool
- Complete a task → Use complete_task tool
- Delete a task → Use delete_task tool (ask for confirmation if unclear)
- Update a task → Use update_task tool

Always confirm actions with a friendly response.
Be conversational and helpful.
"""

def get_or_create_conversation(session: Session, user_id: str, conversation_id: Optional[int] = None) -> Conversation:
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

def load_history(session: Session, conversation_id: int) -> List[dict]:
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

def save_message(session: Session, conversation_id: int, user_id: str, role: str, content: str) -> Message:
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

def run_agent(user_id: str, messages: List[dict]) -> dict:
    """Run OpenAI Agent with MCP tools"""
    try:
        # Get MCP tools
        tools = get_mcp_tools()

        # Add system message
        system_message = {"role": "system", "content": AGENT_INSTRUCTIONS}
        full_messages = [system_message] + messages

        # Call OpenAI with tools
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed to gpt-3.5-turbo for broader compatibility
            messages=full_messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Handle tool calls
        tool_results = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # Execute MCP tool
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Add user_id to tool args
                tool_args["user_id"] = user_id

                # Call the tool
                result = execute_mcp_tool(tool_name, tool_args)
                tool_results.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "result": result
                })

            # If there were tool calls, get final response after tool execution
            if tool_results:
                # For simplicity in this implementation, we'll return the assistant's initial response
                # In a more sophisticated implementation, we would run the agent again with tool results
                return {
                    "response": message.content or "Task completed successfully!",
                    "tool_calls": tool_results
                }

        return {
            "response": message.content or "How can I help you with your tasks?",
            "tool_calls": tool_results
        }

    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "tool_calls": []
        }

def execute_mcp_tool(tool_name: str, args: dict) -> dict:
    """Execute an MCP tool by name"""
    from backend.mcp.server import add_task, list_tasks, complete_task, delete_task, update_task

    tool_map = {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task
    }

    tool_func = tool_map.get(tool_name)
    if not tool_func:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        # Execute the tool function
        result = tool_func(args)
        return result
    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}