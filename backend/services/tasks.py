# [Task]: T-009
# [From]: speckit.plan §2.2

from sqlmodel import Session, select
from ..models import Task
from datetime import datetime
from typing import List, Optional

def create_task(session: Session, user_id: str, title: str, description: str = "") -> Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks(session: Session, user_id: str, status: str = "all") -> List[Task]:
    query = select(Task).where(Task.user_id == user_id)

    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    tasks = session.exec(query).all()
    return tasks

def get_task(session: Session, user_id: str, task_id: int) -> Optional[Task]:
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return None
    return task

def update_task(session: Session, user_id: str, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
    task = get_task(session, user_id, task_id)
    if not task:
        return None

    if title:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, user_id: str, task_id: int) -> bool:
    task = get_task(session, user_id, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def toggle_complete(session: Session, user_id: str, task_id: int) -> Optional[Task]:
    task = get_task(session, user_id, task_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task