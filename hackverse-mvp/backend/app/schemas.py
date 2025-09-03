from pydantic import BaseModel
from typing import Optional, Dict

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'analyst'

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class ThreatEvent(BaseModel):
    source: str
    timestamp: str
    ip: str
    user: str
    event_type: str
    features: Dict[str, float]

class DetectionResult(BaseModel):
    is_threat: bool
    score: float
