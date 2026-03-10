@echo off
chcp 65001 >nul
echo ========================================
echo   ngrok 安全啟動腳本
echo ========================================
echo.

:: 檢查 ngrok 是否已配置
if not exist "%USERPROFILE%\.ngrok2\ngrok.yml" (
    echo [!] 首次運行需要先配置 ngrok
    echo.
    echo 步驟 1: 訪問 https://dashboard.ngrok.com/signup 註冊免費賬戶
    echo 步驟 2: 登錄後複製你的 Authtoken
    echo 步驟 3: 運行以下命令:
    echo.
    echo ngrok config add-authtoken 你的 token
    echo.
    pause
    exit /b 1
)

echo [✓] ngrok 已配置
echo.

:: 設置密碼（可以修改）
set NGROK_USER=admin
set NGROK_PASS=TCG2026!@#

echo ========================================
echo   啟動 ngrok Tunnel
echo ========================================
echo.
echo [信息] 正在啟動 ngrok...
echo [信息] 訪問地址將顯示在下方
echo.
echo [安全提示]
echo - 基本認證：已啟用
echo - 用戶名：%NGROK_USER%
echo - 密碼：%NGROK_PASS%
echo.
echo [!] 重要安全提示:
echo - 不要分享訪問 URL 給他人
echo - 用完請關閉此窗口
echo - 每次重啟 URL 都會改變
echo.
echo 按任意鍵繼續...
pause >nul

echo.
echo ========================================
echo   ngrok 運行中...
echo ========================================
echo.

:: 啟動 ngrok（帶基本認證）
ngrok http 3000 -basic-auth "%NGROK_USER%:%NGROK_PASS%"

echo.
echo ========================================
echo   ngrok 已關閉
echo ========================================
pause
