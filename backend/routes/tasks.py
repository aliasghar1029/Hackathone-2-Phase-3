# [Task]: T-010
# [From]: speckit.plan §3

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session
from ..db import get_session
from ..services import tasks
from ..middleware.jwt import verify_user_id
from typing import List, Optional

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.get("", response_model=List[TaskResponse])
def list_tasks(
    user_id: str,
    status: str = Query("all", regex="^(all|pending|completed)$"),
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    db_tasks = tasks.get_tasks(session, user_id, status)
    # Convert datetime objects to strings for JSON serialization
    result = []
    for task in db_tasks:
        task_dict = task.dict()
        task_dict['created_at'] = task.created_at.isoformat()
        task_dict['updated_at'] = task.updated_at.isoformat()
        result.append(task_dict)
    return result

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    user_id: str,
    data: TaskCreate,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.create_task(session, user_id, data.title, data.description)
    task_dict = task.dict()
    task_dict['created_at'] = task.created_at.isoformat()
    task_dict['updated_at'] = task.updated_at.isoformat()
    return task_dict

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task_dict = task.dict()
    task_dict['created_at'] = task.created_at.isoformat()
    task_dict['updated_at'] = task.updated_at.isoformat()
    return task_dict

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    data: TaskUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.update_task(session, user_id, task_id, data.title, data.description)
    if not task:
        raise HTTPException(404, "Task not found")
    task_dict = task.dict()
    task_dict['created_at'] = task.created_at.isoformat()
    task_dict['updated_at'] = task.updated_at.isoformat()
    return task_dict

@router.delete("/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    success = tasks.delete_task(session, user_id, task_id)
    if not success:
        raise HTTPException(404, "Task not found")
    return {"success": True}

@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verify_user_id)
):
    task = tasks.toggle_complete(session, user_id, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task_dict = task.dict()
    task_dict['created_at'] = task.created_at.isoformat()
    task_dict['updated_at'] = task.updated_at.isoformat()
    return task_dict