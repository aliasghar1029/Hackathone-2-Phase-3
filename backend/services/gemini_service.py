import google.generativeai as genai
import json
from typing import List, Dict, Any

# Configure Gemini
GEMINI_API_KEY = "AIzaSyBAgo7k4uOGTN2LpiSRA3uD93iUm4CKgZA"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-1.5-flash')

# Define tools for Gemini
TOOLS = [
    {
        "name": "add_task",
        "description": "Create a new task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of the task"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "Get all tasks for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["all", "pending", "completed"],
                    "description": "Filter tasks by status"
                }
            }
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to complete"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's title or description",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task"
                }
            },
            "required": ["task_id"]
        }
    }
]

async def chat_with_gemini(
    user_id: str,
    message: str,
    conversation_history: List[Dict[str, str]],
    tool_executor
) -> Dict[str, Any]:
    """
    Send message to Gemini and handle tool calls
    
    Args:
        user_id: The user's ID
        message: User's message
        conversation_history: Previous messages
        tool_executor: Function to execute tools
        
    Returns:
        Dict with response and tool_calls
    """
    try:
        # Build chat history for Gemini
        chat = model.start_chat(history=[])
        
        # Add system instruction
        system_prompt = f"""You are a helpful task management assistant. 
You can help users manage their todo tasks through natural language.

Available tools:
- add_task: Create new tasks
- list_tasks: Show tasks (all, pending, or completed)
- complete_task: Mark tasks as done
- delete_task: Remove tasks
- update_task: Modify tasks

Always be friendly, concise, and confirm actions with emojis like ✓ or ✗.
User ID: {user_id}"""

        # Add conversation history
        for msg in conversation_history:
            if msg["role"] == "user":
                chat.send_message(msg["content"])
        
        # Send current message with tools
        response = chat.send_message(
            message,
            tools=TOOLS
        )
        
        # Check if AI wants to use tools
        tool_calls = []
        final_response = ""
        
        if response.parts:
            for part in response.parts:
                # Check for function calls
                if hasattr(part, 'function_call'):
                    func_call = part.function_call
                    tool_name = func_call.name
                    tool_args = dict(func_call.args)
                    
                    # Add user_id to args
                    tool_args['user_id'] = user_id
                    
                    # Execute tool
                    tool_result = await tool_executor(tool_name, tool_args)
                    
                    tool_calls.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": tool_result
                    })
                    
                    # Generate friendly response based on tool result
                    if tool_name == "add_task":
                        final_response = f"✓ I've added '{tool_args['title']}' to your tasks!"
                    elif tool_name == "list_tasks":
                        tasks = tool_result.get("tasks", [])
                        if not tasks:
                            final_response = "You don't have any tasks yet."
                        else:
                            task_list = "\n".join([
                                f"{i+1}. {t['title']} ({'✓ completed' if t['completed'] else 'pending'})"
                                for i, t in enumerate(tasks)
                            ])
                            final_response = f"Here are your tasks:\n{task_list}"
                    elif tool_name == "complete_task":
                        final_response = f"✓ Task marked as completed!"
                    elif tool_name == "delete_task":
                        final_response = f"✓ Task deleted successfully!"
                    elif tool_name == "update_task":
                        final_response = f"✓ Task updated!"
                        
                elif hasattr(part, 'text'):
                    final_response = part.text
        
        if not final_response:
            final_response = response.text
            
        return {
            "response": final_response,
            "tool_calls": tool_calls
        }
        
    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "tool_calls": []
        }