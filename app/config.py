import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = ".env"

settings = Settings()
