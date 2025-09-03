from typing import Generator
from backend.app.database import SessionLocal
from backend.app.config import Settings

settings = Settings()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_settings():
    return settings
