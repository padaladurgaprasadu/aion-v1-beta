@echo off
echo [AiON] Starting Backend Server (FastAPI)...
start cmd /k "cd /d %~dp0 && pip install -r requirements.txt && python backend/api.py"

echo [AiON] Starting Frontend Server (Vite)...
start cmd /k "cd /d %~dp0\frontend && npm run dev"

echo [AiON] Both servers are starting up in new terminal windows!
echo Please wait a few seconds, then your browser will open automatically...
timeout /t 5 /nobreak >nul
start http://localhost:5173
pause
