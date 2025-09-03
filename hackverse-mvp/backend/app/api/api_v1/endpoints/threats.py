from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas import ThreatEvent, DetectionResult
from backend.app.ml.ensemble import EnsembleAnalyzer
from backend.app.auth import get_current_user

router = APIRouter()

analyzer = EnsembleAnalyzer()

@router.post('/detect')
async def detect(event: ThreatEvent, current_user=Depends(get_current_user)):
    try:
        res = analyzer.analyze(event.dict())
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
