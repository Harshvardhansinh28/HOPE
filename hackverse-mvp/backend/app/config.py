import os
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "HACKVERSE"
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./hackverse.db')
    secret_key: str = os.getenv('HACKVERSE_SECRET', 'change-this-secret')
    access_token_expire_minutes: int = 60
    cors_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = '.env'
