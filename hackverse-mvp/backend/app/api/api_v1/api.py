from fastapi import APIRouter
from backend.app.api.api_v1.endpoints import threats, auth, weights

api_router = APIRouter()
api_router.include_router(threats.router, prefix='/threats', tags=['threats'])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(weights.router, prefix='/weights', tags=['weights'])
