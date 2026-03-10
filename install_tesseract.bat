@echo off
chcp 65001 >nul
echo ========================================
echo   Tesseract OCR 自動安裝程式
echo ========================================
echo.

:: 檢查管理員權限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] 請以管理員身份運行此腳本
    echo.
    echo 右鍵點擊此檔案 -^> 以管理員身份運行
    pause
    exit /b 1
)

echo [✓] 管理員權限已確認
echo.

:: 下載 Tesseract
echo [1/3] 正在下載 Tesseract OCR...
set INSTALLER=%TEMP%\tesseract-installer.exe

powershell -Command "& {Invoke-WebRequest -Uri 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.exe' -OutFile '%INSTALLER%' -UseBasicParsing}"

if exist "%INSTALLER%" (
    echo [✓] 下載完成
) else (
    echo [✗] 下載失敗
    echo.
    echo 請手動下載:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    pause
    exit /b 1
)
echo.

:: 安裝 Tesseract
echo [2/3] 正在安裝 Tesseract OCR...
echo (這可能需要幾分鐘)
"%INSTALLER%" /SILENT /SUPPRESSMSGBOXES /NORESTART /COMPONENTS="extra,basenames"

:: 驗證安裝
echo.
echo [3/3] 驗證安裝...
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [✓] Tesseract OCR 安裝成功!
    echo.
    echo 安裝位置：C:\Program Files\Tesseract-OCR\
    echo.
    
    :: 添加語言包提示
    echo [!] 重要：需要安裝多語言包
    echo.
    echo 請重新運行安裝程式，勾選以下語言包:
    echo   - Chinese - Traditional (繁體中文)
    echo   - Chinese - Simplified (簡體中文)
    echo   - Japanese (日文)
    echo   - Korean (韓文)
    echo.
) else (
    echo [✗] 安裝失敗
    echo.
    echo 請手動安裝：運行 %INSTALLER%
)

echo.
echo ========================================
echo   安裝完成！
echo ========================================
echo.
pause
