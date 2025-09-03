from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.user import Base

engine = create_engine('sqlite:///hackverse.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
