from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from models import Task, TaskCreate, TaskUpdate, User


def get_tasks_by_user_id(session: Session, user_id: str, status: Optional[str] = None) -> List[Task]:
    """
    Get all tasks for a specific user, optionally filtered by status.
    """
    query = select(Task).where(Task.user_id == user_id)
    
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
    elif status != "all" and status is not None:
        # If status is provided but not 'all', 'pending', or 'completed', raise an error
        raise ValueError("Status must be 'all', 'pending', or 'completed'")
    
    # Order by created_at descending (newest first)
    query = query.order_by(Task.created_at.desc())
    
    return session.exec(query).all()


def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a user.
    """
    # Validate title
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise ValueError("Title is required")
    
    if len(task_data.title) > 200:
        raise ValueError("Title too long (max 200 characters)")
    
    # Validate description if provided
    if task_data.description and len(task_data.description) > 1000:
        raise ValueError("Description too long (max 1000 characters)")
    
    # Create task
    db_task = Task(
        title=task_data.title.strip(),
        description=task_data.description,
        completed=False,
        user_id=user_id
    )
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


def update_task(session: Session, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """
    Update a task if it belongs to the user.
    """
    # Get the task
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    
    if not task:
        return None
    
    # Check if task belongs to user
    if task.user_id != user_id:
        raise PermissionError("Task does not belong to user")
    
    # Validate title if provided
    if task_update.title is not None:
        if len(task_update.title) == 0:
            raise ValueError("Title cannot be empty")
        
        if len(task_update.title) > 200:
            raise ValueError("Title too long (max 200 characters)")
        
        task.title = task_update.title.strip()
    
    # Validate description if provided
    if task_update.description is not None:
        if len(task_update.description) > 1000:
            raise ValueError("Description too long (max 1000 characters)")
        
        task.description = task_update.description
    
    # Update timestamps
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task if it belongs to the user.
    """
    # Get the task
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    
    if not task:
        return False
    
    # Check if task belongs to user
    if task.user_id != user_id:
        raise PermissionError("Task does not belong to user")
    
    session.delete(task)
    session.commit()
    
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task if it belongs to the user.
    """
    # Get the task
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    
    if not task:
        return None
    
    # Check if task belongs to user
    if task.user_id != user_id:
        raise PermissionError("Task does not belong to user")
    
    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task