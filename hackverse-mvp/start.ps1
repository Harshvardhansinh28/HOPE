# Start backend locally
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
.\.venv\Scripts\uvicorn.exe backend.app.main:app --reload --host 0.0.0.0 --port 8000
