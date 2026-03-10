# 🚀 全自動部署最終指南

## 已完成 ✅

- [x] GitHub Pages 已啟用
- [x] 前端部署 Workflow 已創建 (`deploy-pages.yml`)
- [x] 環境變量 `VITE_API_URL` 已設置
- [x] 後端部署 Workflow 已創建 (`deploy-railway.yml`)

---

## ⚠️ 需要完成的步驟（5 分鐘）

### 步驟 1：生成 Railway API Token

1. 訪問：**https://railway.com/account/tokens**
2. 點擊 **New Token**
3. 給 Token 起個名字（例如：`tcg-price-app`）
4. 點擊 **Create**
5. **複製 Token**（只顯示一次！）

### 步驟 2：添加到 GitHub Secrets

1. 訪問：**https://github.com/felixaiclaw-svg/tcg-price-app/settings/secrets/actions**
2. 點擊 **New repository secret**
3. 添加：
   - **Name**: `RAILWAY_TOKEN`
   - **Value**: 粘貼剛才複製的 Token
4. 點擊 **Add secret**

### 步驟 3：在 Railway 創建項目

1. 訪問：**https://railway.com**
2. 登錄（用 GitHub 賬號）
3. 點擊 **New Project** → **Deploy from GitHub repo**
4. 選擇 `felixaiclaw-svg/tcg-price-app`
5. Railway 會自動檢測 `backend/` 目錄
6. 等待部署完成

### 步驟 4：獲取後端 URL 並更新

1. 在 Railway Dashboard 點擊你的項目
2. 複製 **Public URL**（格式：`https://xxx.up.railway.app`）
3. 訪問：**https://github.com/felixaiclaw-svg/tcg-price-app/settings/variables/actions**
4. 編輯 `VITE_API_URL`，改為你的 Railway URL
5. 保存

### 步驟 5：觸發部署

1. 訪問：**https://github.com/felixaiclaw-svg/tcg-price-app/actions**
2. 點擊 **Deploy to GitHub Pages** → **Run workflow**
3. 點擊 **Deploy Backend to Railway** → **Run workflow**（可選，Railway 會自動部署）

---

## 🎉 完成後

| 組件 | URL |
|------|-----|
| 前端 | https://felixaiclaw-svg.github.io/tcg-price-app/ |
| 後端 | https://你的-app.up.railway.app |

---

## 📝 注意事項

1. **Railway 免費額度**：每月 $5 點數，對於小型應用足夠
2. **自動部署**：每次 push 到 master 分支都會自動部署
3. **HTTPS**：兩個平台都自動提供 HTTPS

---

## ❓ 需要幫助？

如果遇到問題，請告訴我具體哪一步出錯！
