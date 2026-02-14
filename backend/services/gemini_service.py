import google.generativeai as genai
from typing import List, Dict, Any
import os

# Configure Gemini with API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBAgo7k4uOGTN2LpiSRA3uD93iUm4CKgZA")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-1.5-flash')

def chat_with_gemini(
    user_id: str,
    message: str,
    conversation_history: List[Dict[str, str]],
    tool_executor
) -> Dict[str, Any]:
    """Send message to Gemini and execute tools"""

    try:
        # System prompt for Gemini
        system_prompt = f"""You are a helpful task management assistant.
You help users manage their todo tasks through conversation.

When user wants to:
- Add/create a task → use add_task tool
- Show/list tasks → use list_tasks tool
- Complete/finish/done a task → use complete_task tool
- Delete/remove a task → use delete_task tool
- Update/change a task → use update_task tool

Always be friendly and confirm actions with ✓ emoji.
Keep responses concise and clear.

User ID: {user_id}"""

        # Simple response without tools for now
        # (Gemini function calling needs specific setup)

        # For MVP, we'll use simple keyword detection
        message_lower = message.lower()

        # Detect intent and execute tool
        if any(word in message_lower for word in ['add', 'create', 'new task', 'remember']):
            # Extract task title (simple approach)
            title = message.replace('add task', '').replace('create task', '').replace('add a task', '').replace('to', '').strip()
            if not title:
                title = message

            result = tool_executor('add_task', {
                'user_id': user_id,
                'title': title,
                'description': ''
            })

            return {
                'response': f"✓ I've added '{title}' to your tasks!",
                'tool_calls': [{'tool': 'add_task', 'result': result}]
            }

        elif any(word in message_lower for word in ['show', 'list', 'see', 'what', 'my tasks']):
            # Detect status filter
            if 'pending' in message_lower:
                status = 'pending'
            elif 'completed' in message_lower or 'done' in message_lower:
                status = 'completed'
            else:
                status = 'all'

            result = tool_executor('list_tasks', {
                'user_id': user_id,
                'status': status
            })

            tasks = result.get('tasks', [])
            if not tasks:
                response = "You don't have any tasks yet."
            else:
                task_list = "\n".join([
                    f"{i+1}. {t['title']} ({'✓ completed' if t['completed'] else 'pending'})"
                    for i, t in enumerate(tasks)
                ])
                response = f"Here are your tasks:\n{task_list}"

            return {
                'response': response,
                'tool_calls': [{'tool': 'list_tasks', 'result': result}]
            }

        elif any(word in message_lower for word in ['complete', 'done', 'finish', 'mark']):
            # Extract task ID (simple approach - look for numbers)
            import re
            numbers = re.findall(r'\d+', message)
            if numbers:
                task_id = int(numbers[0])
                result = tool_executor('complete_task', {
                    'user_id': user_id,
                    'task_id': task_id
                })
                return {
                    'response': f"✓ Task {task_id} marked as completed!",
                    'tool_calls': [{'tool': 'complete_task', 'result': result}]
                }
            else:
                return {
                    'response': "Please specify which task number to complete (e.g., 'complete task 1')",
                    'tool_calls': []
                }

        elif any(word in message_lower for word in ['delete', 'remove']):
            # Extract task ID
            import re
            numbers = re.findall(r'\d+', message)
            if numbers:
                task_id = int(numbers[0])
                result = tool_executor('delete_task', {
                    'user_id': user_id,
                    'task_id': task_id
                })
                return {
                    'response': f"✓ Task {task_id} deleted successfully!",
                    'tool_calls': [{'tool': 'delete_task', 'result': result}]
                }
            else:
                return {
                    'response': "Please specify which task number to delete (e.g., 'delete task 1')",
                    'tool_calls': []
                }

        else:
            # Default response
            return {
                'response': "I can help you manage tasks! Try: 'add a task', 'show my tasks', 'complete task 1', or 'delete task 2'",
                'tool_calls': []
            }

    except Exception as e:
        print(f"Gemini error: {e}")
        return {
            'response': f"Sorry, I encountered an error: {str(e)}",
            'tool_calls': []
        }