@echo off
chcp 65001 >nul
echo ========================================
echo   TCG Price Scanner - 一鍵啟動
echo ========================================
echo.

:: 獲取本機 IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do set LOCAL_IP=%%b
)
echo 本機 IP: %LOCAL_IP%
echo.

:: 檢查後端
echo [1/3] 啟動後端服務...
cd /d "%~dp0backend"
start "TCG Backend" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo [✓] 後端已啟動
echo     本機：http://localhost:8000
echo     局域網：http://%LOCAL_IP%:8000
echo.

:: 檢查前端
echo [2/3] 啟動前端服務...
cd /d "%~dp0frontend"
start "TCG Frontend" cmd /k "npm run dev -- --host 0.0.0.0"
echo [✓] 前端已啟動
echo     本機：http://localhost:3000
echo     局域網：http://%LOCAL_IP%:3000
echo.

:: 顯示訪問信息
echo ========================================
echo   服務已啟動！
echo ========================================
echo.
echo   訪問地址:
echo   • 本機電腦：http://localhost:3000
echo   • 手機（同 WiFi）：http://%LOCAL_IP%:3000
echo.
echo   API 文檔：http://localhost:8000/docs
echo   健康檢查：http://localhost:8000/api/v1/health
echo.
echo   按任意鍵退出...
echo   (後台服務繼續運行)
pause >nul
