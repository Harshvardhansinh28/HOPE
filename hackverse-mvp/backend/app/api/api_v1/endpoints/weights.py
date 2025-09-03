from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.app.ml.ensemble import AgentWeight
from backend.app.ml.agents import ALL_AGENTS
from backend.app.database import SessionLocal, init_db
from backend.app.auth import require_role, get_current_user

router = APIRouter()


@router.get('/', response_model=List[dict])
def list_weights(current_user=Depends(get_current_user)):
    db = SessionLocal()
    items = []
    try:
        for w in db.query(AgentWeight).all():
            items.append({'technique': w.technique, 'weight': float(w.weight)})
    finally:
        db.close()
    # if empty, return defaults
    if not items:
        items = [{'technique': a.technique, 'weight': 1.0} for a in ALL_AGENTS]
    return items


@router.put('/{technique}')
def update_weight(technique: str, payload: dict, current_user=Depends(require_role('admin'))):
    if 'weight' not in payload:
        raise HTTPException(status_code=400, detail='weight required')
    wval = float(payload['weight'])
    db = SessionLocal()
    try:
        w = db.query(AgentWeight).filter(AgentWeight.technique == technique).first()
        if not w:
            w = AgentWeight(technique=technique, weight=wval)
            db.add(w)
        else:
            w.weight = wval
        db.commit()
    finally:
        db.close()
    return {'technique': technique, 'weight': wval}


@router.post('/reset')
def reset_weights(current_user=Depends(require_role('admin'))):
    # create table and seed defaults
    init_db()
    db = SessionLocal()
    try:
        # clear existing
        db.query(AgentWeight).delete()
        for a in ALL_AGENTS:
            db.add(AgentWeight(technique=a.technique, weight=1.0))
        db.commit()
    finally:
        db.close()
    return {'status': 'seeded'}
