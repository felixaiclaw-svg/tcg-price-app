@echo off
echo ========================================
echo   TCG Price App - Cloudflare Pages 部署
echo ========================================
echo.

cd frontend

echo [1/3] 安裝依賴...
call npm install

echo.
echo [2/3] 構建前端...
call npm run build

echo.
echo [3/3] 部署到 Cloudflare Pages...
echo.
echo 請確認已執行：wrangler login
echo.
pause

wrangler pages deploy dist --project-name=tcg-price-app

echo.
echo ========================================
echo   部署完成！
echo ========================================
echo.
echo 訪問地址：https://tcg-price-app.pages.dev
echo.
pause
