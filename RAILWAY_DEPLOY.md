# 🚀 Railway 部署指南（5 分鐘完成）

## ✅ 已完成

- [x] GitHub Repo 創建：https://github.com/felixaiclaw-svg/tcg-price-app
- [x] 代碼已推送
- [x] GitHub Actions 自動部署配置

---

## 📋 Railway 部署步驟

### 1️⃣ 登入 Railway

訪問：https://railway.app

**使用 GitHub 登入**（這樣可以授權訪問你的 repo）

### 2️⃣ 創建新項目

1. 點擊 **"New Project"**
2. 選擇 **"Deploy from GitHub repo"**
3. 選擇 **`felixaiclaw-svg/tcg-price-app`**
4. Railway 會自動檢測並開始部署

### 3️⃣ 設置後端目錄

1. 點擊剛創建的項目
2. 進入 **"Settings"** 標籤
3. 找到 **"Root Directory"**
4. 輸入：`backend`
5. 按 Enter 保存

### 4️⃣ 設置環境變量

1. 點擊 **"Variables"** 標籤
2. 點擊 **"New Variable"**
3. 添加以下變量：

```
GEMINI_API_KEY = 從 tcg-price-app/backend/.env 複製你的 API Key
PORT = 8000
HOST = 0.0.0.0
```

4. Railway 會自動重新部署

### 5️⃣ 獲取部署 URL

部署完成後（約 2-3 分鐘）：

1. 點擊 **"Settings"**
2. 找到 **"Networking"** 或 **"Domains"**
3. 你會看到類似：`https://tcg-price-app-production.up.railway.app`
4. **複製這個 URL**

---

## 🔗 綁定自定義域名（api.ecoxlabs.com）

### 在 Railway 設置

1. 在項目頁面點擊 **"Settings"**
2. 找到 **"Domains"**
3. 點擊 **"Add Custom Domain"**
4. 輸入：`api.ecoxlabs.com`
5. Railway 會顯示 DNS 記錄

### 在 Dynadot 添加 DNS

1. 登入 Dynadot
2. 進入 `ecoxlabs.com` DNS 設置
3. 添加記錄：

```
類型：CNAME
主機/名稱：api
目標值：你的-railway-url.up.railway.app
TTL：自動
```

---

## 🔧 更新前端 API 地址

### 在 Vercel 設置

1. 訪問：https://vercel.com/felixaiclaw-svgs-projects/frontend/settings/environment-variables
2. 點擊 **"Add"**
3. 添加：
   - **Key**: `VITE_API_URL`
   - **Value**: `https://api.ecoxlabs.com`（或 Railway URL）
4. 點擊 **"Save"**
5. Vercel 會自動重新部署

---

## ✅ 完成後測試

訪問：https://www.ecoxlabs.com

上傳卡牌圖片測試 AI 識別功能！

---

## 🎯 快速檢查清單

- [ ] Railway 項目已創建
- [ ] Root Directory 設置為 `backend`
- [ ] 環境變量已設置（GEMINI_API_KEY, PORT）
- [ ] 獲取 Railway 部署 URL
- [ ] 綁定 `api.ecoxlabs.com` 域名
- [ ] Dynadot DNS 已設置
- [ ] Vercel `VITE_API_URL` 已更新
- [ ] 測試完整功能

---

**完成每一步後告訴我，我會幫你檢查！** 🚀
