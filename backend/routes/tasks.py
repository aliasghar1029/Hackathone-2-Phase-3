from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from typing import List
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from db import get_session
from models import Task, TaskCreate, TaskUpdate, TaskRead, User
from middleware.jwt import get_current_user, validate_user_id_match
from services.tasks import (
    get_tasks_by_user_id,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)

router = APIRouter(tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_tasks(
    user_id: str,
    status_param: str = "all",
    token_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all tasks for a user, optionally filtered by status.
    Requires Authorization: Bearer {token} header.
    """
    # Validate that URL user_id matches token user_id
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    try:
        # Using the async service functions
        result = await session.execute(
            select(Task).where(Task.user_id == user_id)
        )
        tasks = result.scalars().all()

        if status_param != "all":
            if status_param == "completed":
                tasks = [task for task in tasks if task.completed]
            elif status_param == "pending":
                tasks = [task for task in tasks if not task.completed]

        # Convert datetime objects to ISO format strings for JSON serialization
        task_list = []
        for task in tasks:
            task_dict = task.model_dump()
            task_dict['created_at'] = task.created_at.isoformat()
            task_dict['updated_at'] = task.updated_at.isoformat()
            task_list.append(TaskRead(**task_dict))

        return task_list
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task_data: TaskCreate,
    token_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    Requires Authorization: Bearer {token} header.
    """
    # Validate that URL user_id matches token user_id
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only create tasks for yourself"
        )

    try:
        # Create new task
        db_task = Task(
            **task_data.model_dump(),
            user_id=user_id
        )

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        # Convert datetime objects to ISO format strings for JSON serialization
        task_dict = db_task.model_dump()
        task_dict['created_at'] = db_task.created_at.isoformat()
        task_dict['updated_at'] = db_task.updated_at.isoformat()

        return TaskRead(**task_dict)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    token_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update an existing task.
    Requires Authorization: Bearer {token} header.
    """
    # Validate that URL user_id matches token user_id
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    try:
        # Get the task
        result = await session.execute(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        )
        db_task = result.scalar_one_or_none()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update the task
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        await session.commit()
        await session.refresh(db_task)

        # Convert datetime objects to ISO format strings for JSON serialization
        task_dict = db_task.model_dump()
        task_dict['created_at'] = db_task.created_at.isoformat()
        task_dict['updated_at'] = db_task.updated_at.isoformat()

        return TaskRead(**task_dict)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_existing_task(
    user_id: str,
    task_id: int,
    token_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete an existing task.
    Requires Authorization: Bearer {token} header.
    """
    # Validate that URL user_id matches token user_id
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only delete your own tasks"
        )

    # Get the task
    result = await session.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    )
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await session.delete(db_task)
    await session.commit()

    return {"success": True}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    token_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    Requires Authorization: Bearer {token} header.
    """
    # Validate that URL user_id matches token user_id
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    # Get the task
    result = await session.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    )
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    db_task.completed = not db_task.completed
    await session.commit()
    await session.refresh(db_task)

    # Convert datetime objects to ISO format strings for JSON serialization
    task_dict = db_task.model_dump()
    task_dict['created_at'] = db_task.created_at.isoformat()
    task_dict['updated_at'] = db_task.updated_at.isoformat()

    return TaskRead(**task_dict)