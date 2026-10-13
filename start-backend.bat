@echo off
setlocal
cd /d "%~dp0backend"
if not exist .venv\Scripts\python.exe (
  echo Creating Python virtual environment...
  python -m venv .venv
  if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo Starting Academy API at http://127.0.0.1:8000
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
goto end
:error
echo Could not start the API. Ensure Python 3.11+ is installed and available as python.
pause
:end
endlocal
