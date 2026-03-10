@echo off
echo ========================================
echo   TCG Price Scanner - 快速啟動腳本
echo ========================================
echo.

:: 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 Python，請先安裝 Python 3.9+
    pause
    exit /b 1
)
echo [✓] Python 已安裝

:: 檢查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 Node.js，請先安裝 Node.js 18+
    pause
    exit /b 1
)
echo [✓] Node.js 已安裝

echo.
echo ========================================
echo   正在啟動後端服務...
echo ========================================
echo.

cd backend

:: 檢查依賴
if not exist "venv" (
    echo [信息] 創建虛擬環境...
    python -m venv venv
)

call venv\Scripts\activate.bat

:: 安裝依賴
echo [信息] 檢查依賴...
pip install -q -r requirements.txt

:: 啟動後端
echo [信息] 啟動後端服務 (端口 8000)...
start "TCG Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [✓] 後端服務已啟動
echo.

cd ..\frontend

echo ========================================
echo   正在啟動前端服務...
echo ========================================
echo.

:: 檢查依賴
if not exist "node_modules" (
    echo [信息] 安裝前端依賴 (這可能需要幾分鐘)...
    call npm install
)

:: 啟動前端
echo [信息] 啟動前端服務 (端口 3000)...
start "TCG Frontend" cmd /k "npm run dev"

echo [✓] 前端服務已啟動
echo.

echo ========================================
echo   啟動完成！
echo ========================================
echo.
echo   網頁訪問：http://localhost:3000
echo   API 文檔：http://localhost:8000/docs
echo.
echo   按任意鍵退出此窗口...
echo   (後端和前端將在獨立窗口繼續運行)
pause >nul
