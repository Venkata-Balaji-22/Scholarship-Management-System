# Agentic AI - Scholarship Opportunities

A small Agentic AI system using FastAPI (recommendations API), Flask (auth + UI hosting), and LangChain tools to recommend scholarships based on student academic details. Includes registration/login (JWT), modern UI, and direct links to apply.

## Features
- FastAPI API at `http://127.0.0.1:8001` with `/recommend`
- Flask Auth + UI at `http://127.0.0.1:5001` with `/login`, `/register`, `/logout`, and UI at `/ui`
- LangChain tools for scholarship listing and filtering
- SQLite via SQLAlchemy for user accounts
- Modern glassmorphism UI

## Requirements
- Python 3.10+
- Windows PowerShell

## Setup
1. Open PowerShell in the project root: `agentic-scholarships/`
2. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env` and change secrets if desired.

## Run
Open two PowerShell windows, activate the venv in both.

1) Start Flask (Auth + UI):
```powershell
$env:FLASK_PORT=5001
python -m flask_auth.app
```
- Visit `http://127.0.0.1:5001/ui` for the UI
- Use `Login`/`Register` links to create an account and log in

2) Start FastAPI (API):
```powershell
$env:API_PORT=8001
uvicorn fastapi_app.main:app --host 127.0.0.1 --port $env:API_PORT --reload
```
- Health check: `http://127.0.0.1:8001/`

## How it works
- Login sets two cookies: `access_token` (HTTP-only) and `access_token_js` (JS-readable for demo). The frontend uses `Authorization: Bearer <token>` to call FastAPI `/recommend`.
- The agent (`fastapi_app/agent.py`) uses LangChain tools to filter the data in `fastapi_app/scholarship_data.py`.

## Using the app
- For Engineering track: provide 10th, Intermediate, and (optionally) B.Tech CGPA plus income/category/state.
- For Intermediate track: provide 10th CGPA (others optional) plus income/category/state.
- Click "Find Scholarships" to get matching results and open their application URLs.

## Notes
- Replace example scholarship URLs with real ones.
- If you have an OpenAI API key, set `OPENAI_API_KEY` in `.env` and extend the agent to use an LLM policy for tool selection.
- For production, serve the UI via a proper web server and secure cookies/domains.
