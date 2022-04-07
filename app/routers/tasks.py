from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from .. import models, schemas
from ..crud import tasks as crud


router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=List[schemas.Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return crud.get_tasks(db, user_id=user.id, skip=skip, limit=limit)


@router.post("/tasks", status_code=201, response_model=schemas.Task)
def create_task(
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return crud.create_task(db, user_id=user.id, task=task_data)


@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    if task.owner_id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return task


@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    if task.owner_id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return crud.update_task(db, task_id=task_id, task=task_data)


@router.delete("/tasks/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    if task.owner_id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return crud.delete_task(db, task_id=task_id)
