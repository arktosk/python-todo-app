from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import config, security, schemas
from .crud.users import get_user
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_payload = schemas.TokenPayload(sub=int(sub))
    except JWTError:
        raise credentials_exception
    if token_payload.sub is None:
        raise credentials_exception
    user = get_user(db, user_id=token_payload.sub)
    if user is None:
        raise credentials_exception
    return user
