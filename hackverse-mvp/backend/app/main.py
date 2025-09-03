from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.api_v1.api import api_router
from backend.app.config import Settings
from pydantic import BaseModel
from backend.app.ml.anomaly_detector import AnomalyDetector
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.auth import authenticate_user, create_access_token, Token
from backend.app.auth import get_current_user, require_role
from backend.app.database import SessionLocal, init_db
from backend.app.models.user import User


# initialize sqlite DB
init_db()

settings = Settings()
app = FastAPI(title=settings.app_name)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include api router
app.include_router(api_router, prefix='/api/v1')

class Event(BaseModel):
    source: str
    timestamp: str
    ip: str
    user: str
    event_type: str
    features: dict

# simple in-memory detector instance
detector = AnomalyDetector()

@app.post('/api/v1/threats/detect')
async def detect(event: Event, current_user: User = Depends(get_current_user)):
    features = list(event.features.values())
    try:
        score = detector.score([features])[0]
        is_anom = detector.is_anomaly(score)
        return {"is_threat": bool(is_anom), "score": float(score)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/api/v1/auth/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str = 'analyst'


@app.post('/api/v1/users', status_code=201)
async def create_user(req: CreateUserRequest, current_user: User = Depends(require_role('admin'))):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail='User exists')
    from backend.app.auth import get_password_hash
    user = User(username=req.username, hashed_password=get_password_hash(req.password), role=req.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"id": user.id, "username": user.username, "role": user.role}

@app.get('/')
async def root():
    return {"status": "ok"}
