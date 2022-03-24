from typing import Optional
from sqlalchemy.orm import Session

from . import models, schemas, security


def authenticate_user(db: Session, user_email: str, password: str):
    db_user = get_user_by_email(db, email=user_email)
    if not db_user:
        return False
    if not security.verify_password(password, db_user.hashed_password):
        return False
    return db_user


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Todo)
        .filter(models.Todo.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_todo(db: Session, user_id: int, todo: schemas.TodoCreate) -> schemas.Todo:
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int) -> Optional[schemas.Todo]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def update_todo(
    db: Session, todo_id: int, todo: schemas.TodoCreate
) -> Optional[schemas.Todo]:
    db_todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .first()
    )
    if db_todo is not None:
        setattr(db_todo, "title", todo.title)
        setattr(db_todo, "description", todo.description)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> Optional[schemas.Todo]:
    db_todo = db.query(models.Todo).get(todo_id)
    db.delete(db_todo)
    db.commit()
    return db_todo
