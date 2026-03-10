@echo off
chcp 65001 >nul
echo ========================================
echo   TCG Price Scanner - 啟動服務
echo ========================================
echo.

:: 獲取本機 IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do set LOCAL_IP=%%b
)
echo 本機 IP: %LOCAL_IP%
echo.

:: 啟動後端
echo [1/2] 啟動後端服務...
cd /d "%~dp0backend"
start "TCG Backend" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo [✓] 後端已啟動
echo     http://localhost:8000
echo     http://%LOCAL_IP%:8000
echo.

:: 啟動前端
echo [2/2] 啟動前端服務...
cd /d "%~dp0frontend"
start "TCG Frontend" cmd /k "npm run dev -- --host 0.0.0.0"
echo [✓] 前端已啟動
echo     http://localhost:3000
echo     http://%LOCAL_IP%:3000
echo.

echo ========================================
echo   服務已啟動！
echo ========================================
echo.
echo   電腦訪問:
echo   http://localhost:3000
echo.
echo   手機訪問 (同一 WiFi):
echo   http://%LOCAL_IP%:3000
echo.
echo   按任意鍵退出...
pause >nul
