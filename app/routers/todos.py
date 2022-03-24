from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from .. import crud, models, schemas


router = APIRouter(tags=["todos"])


@router.get("/todos", response_model=List[schemas.Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return crud.get_todos(db, user_id=user.id, skip=skip, limit=limit)


@router.post("/todos", status_code=201, response_model=schemas.Todo)
def create_todo(
    todo_data: schemas.TodoCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return crud.create_todo(db, user_id=user.id, todo=todo_data)


@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    todo = crud.get_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner_id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return todo


@router.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    todo_data: schemas.TodoCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    todo = crud.get_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner_id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return crud.update_todo(db, todo_id=todo_id, todo=todo_data)


@router.delete("/todos/{todo_id}")
def remove_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    todo = crud.get_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.owner_id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return crud.delete_todo(db, todo_id=todo_id)
