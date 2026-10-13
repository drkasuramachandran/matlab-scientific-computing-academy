@echo off
setlocal
cd /d "%~dp0frontend"
where node >nul 2>nul || (echo Node.js 20+ is required. Install it from https://nodejs.org/ & pause & exit /b 1)
if not exist node_modules (
  echo Installing frontend packages...
  call npm install
  if errorlevel 1 goto error
)
if not exist .env.local copy .env.example .env.local >nul
echo Starting website at http://localhost:3000
call npm run dev
goto end
:error
echo Frontend setup failed. Check the Node.js/npm installation and internet connection.
pause
:end
endlocal
