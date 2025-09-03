HACKVERSE MVP

This is a minimal, runnable skeleton of the HACKVERSE cybersecurity MVP tailored to integrate with n8n.

What's included

- FastAPI backend: `backend/app/main.py`
- SQLAlchemy models: `backend/app/models/` (users, threats)
- ML module: `backend/app/ml/anomaly_detector.py` (IsolationForest)
- Simple API endpoint: POST /api/v1/threats/detect
- Dockerfile and docker-compose for local testing
- n8n workflow JSON for integration

Quick run (locally)

# Linux / WSL / macOS
python -m venv .venv; .venv/bin/pip install -r requirements.txt; uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Windows PowerShell
python -m venv .venv; .\.venv\Scripts\pip.exe install -r requirements.txt; .\.venv\Scripts\uvicorn.exe backend.app.main:app --reload --host 0.0.0.0 --port 8000

Docs
- API docs: http://localhost:8000/docs

Notes
- This is a starter skeleton. Extend models, auth, background workers, and CI/CD as needed.
