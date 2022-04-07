from typing import Optional
from sqlalchemy.orm import Session

from .. import models, schemas


def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Task)
        .filter(models.Task.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_task(db: Session, user_id: int, task: schemas.TaskCreate) -> schemas.Task:
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[schemas.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(
    db: Session, task_id: int, task: schemas.TaskCreate
) -> Optional[schemas.Task]:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is not None:
        setattr(db_task, "title", task.title)
        setattr(db_task, "description", task.description)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> Optional[schemas.Task]:
    db_task = db.query(models.Task).get(task_id)
    db.delete(db_task)
    db.commit()
    return db_task
