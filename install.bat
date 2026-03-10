@echo off
chcp 65001 >nul
echo ========================================
echo   TCG Price Scanner - 完整安裝程式
echo ========================================
echo.

:: 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 Python
    echo 請先安裝 Python 3.9+: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [✓] Python 已安裝
echo.

:: 檢查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 Node.js
    echo 請先安裝 Node.js 18+: https://nodejs.org/
    pause
    exit /b 1
)
echo [✓] Node.js 已安裝
echo.

:: 檢查 Tesseract
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [✓] Tesseract OCR 已安裝
) else (
    echo [!] Tesseract OCR 未安裝
    echo.
    echo 請按照以下步驟安裝:
    echo 1. 訪問：https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. 下載最新安裝程式
    echo 3. 安裝時勾選語言包:
    echo    - Chinese - Traditional (繁體中文)
    echo    - Chinese - Simplified (簡體中文)
    echo    - Japanese (日文)
    echo    - Korean (韓文)
    echo.
    echo 安裝完成後重新運行此腳本
    pause
    goto :INSTALL_SOFTWARE
)
echo.

:INSTALL_SOFTWARE
echo ========================================
echo   安裝軟體依賴
echo ========================================
echo.

:: 安裝 Python 依賴
echo [1/3] 安裝 Python 依賴...
cd /d "%~dp0backend"
if exist "venv" (
    echo 使用現有虛擬環境
) else (
    echo 創建虛擬環境...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo [✓] Python 依賴安裝完成
echo.

:: 安裝 Node 依賴
echo [2/3] 安裝 Node 依賴...
cd /d "%~dp0frontend"
if exist "node_modules" (
    echo 更新現有依賴
) else (
    echo 安裝新依賴...
)
call npm install --silent
echo [✓] Node 依賴安裝完成
echo.

:: 啟動服務
echo ========================================
echo   啟動服務
echo ========================================
echo.

echo [3/3] 啟動後端和前端服務...
echo.

:: 啟動後端
cd /d "%~dp0backend"
start "TCG Backend" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo [✓] 後端服務已啟動 (http://localhost:8000)

:: 啟動前端
cd /d "%~dp0frontend"
start "TCG Frontend" cmd /k "npm run dev"
echo [✓] 前端服務已啟動 (http://localhost:3000)

echo.
echo ========================================
echo   安裝完成！
echo ========================================
echo.
echo   訪問地址:
echo   • 網頁版：http://localhost:3000
echo   • API 文檔：http://localhost:8000/docs
echo   • 健康檢查：http://localhost:8000/api/v1/health
echo.
echo   按任意鍵退出...
pause >nul
