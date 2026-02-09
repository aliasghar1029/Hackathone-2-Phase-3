# [Task]: T-011 & T-012
# [From]: speckit.plan §2.2 & speckit.specify §8

from mcp import MCPServer, Tool
from pydantic import BaseModel
from sqlmodel import Session
from ..services import tasks as task_service
from ..db import engine
import uuid


# Initialize MCP server
mcp_server = MCPServer(name="todo-mcp-server")

# Tool schemas
class AddTaskInput(BaseModel):
    user_id: str
    title: str
    description: str = ""


class ListTasksInput(BaseModel):
    user_id: str
    status: str = "all"


class TaskActionInput(BaseModel):
    user_id: str
    task_id: int


class UpdateTaskInput(BaseModel):
    user_id: str
    task_id: int
    title: str = None
    description: str = None


@mcp_server.tool()
def add_task(input: AddTaskInput) -> dict:
    """Create a new task"""
    try:
        with Session(engine) as session:
            task = task_service.create_task(
                session,
                input.user_id,
                input.title,
                input.description
            )
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
    except Exception as e:
        return {"error": str(e)}


@mcp_server.tool()
def list_tasks(input: ListTasksInput) -> dict:
    """List tasks with optional status filter"""
    try:
        with Session(engine) as session:
            db_tasks = task_service.get_tasks(session, input.user_id, input.status)
            return {
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "completed": t.completed,
                        "created_at": str(t.created_at)
                    }
                    for t in db_tasks
                ]
            }
    except Exception as e:
        return {"error": str(e)}


@mcp_server.tool()
def complete_task(input: TaskActionInput) -> dict:
    """Mark a task as complete"""
    try:
        with Session(engine) as session:
            task = task_service.toggle_complete(session, input.user_id, input.task_id)
            if not task:
                return {"error": "Task not found"}
            return {
                "task_id": task.id,
                "status": "completed" if task.completed else "incomplete",
                "title": task.title
            }
    except Exception as e:
        return {"error": str(e)}


@mcp_server.tool()
def delete_task(input: TaskActionInput) -> dict:
    """Delete a task"""
    try:
        with Session(engine) as session:
            # Get task title before deleting
            task = task_service.get_task(session, input.user_id, input.task_id)
            if not task:
                return {"error": "Task not found"}

            title = task.title
            success = task_service.delete_task(session, input.user_id, input.task_id)

            if success:
                return {
                    "task_id": input.task_id,
                    "status": "deleted",
                    "title": title
                }
            return {"error": "Delete failed"}
    except Exception as e:
        return {"error": str(e)}


@mcp_server.tool()
def update_task(input: UpdateTaskInput) -> dict:
    """Update task title or description"""
    try:
        with Session(engine) as session:
            task = task_service.update_task(
                session,
                input.user_id,
                input.task_id,
                input.title,
                input.description
            )
            if not task:
                return {"error": "Task not found"}
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
    except Exception as e:
        return {"error": str(e)}


def get_mcp_tools():
    """Return MCP tools for OpenAI Agent"""
    return mcp_server.get_tools()