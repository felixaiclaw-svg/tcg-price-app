# 🚀 後端部署指南（Railway）

## ✅ 前端狀態
- **域名**: www.ecoxlabs.com ✅
- **SSL**: 生成中（5-10 分鐘）
- **狀態**: Production

---

## 📦 部署後端到 Railway

### 方法 1：GitHub 自動部署（推薦）

#### 1️⃣ 將代碼推送到 GitHub

```powershell
# 在項目根目錄執行
cd C:\Users\felix\.openclaw\workspace\tcg-price-app

# 初始化 git（如果還沒有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - TCG Price App"

# 在 GitHub 創建空 repo，然後：
git remote add origin https://github.com/你的用戶名/tcg-price-app.git
git push -u origin main
```

#### 2️⃣ 在 Railway 部署

1. 訪問：https://railway.app
2. 點擊 **"Login"** → 用 **GitHub 登入**
3. 點擊 **"New Project"**
4. 選擇 **"Deploy from GitHub repo"**
5. 選擇 `tcg-price-app` repo
6. Railway 會自動檢測並部署

#### 3️⃣ 設置環境變量

在 Railway 項目頁面：

1. 點擊 **"Variables"** 標籤
2. 添加以下變量：

```
GEMINI_API_KEY = 從 tcg-price-app/backend/.env 複製你的 API Key
PORT = 8000
HOST = 0.0.0.0
```

3. Railway 會自動重新部署

#### 4️⃣ 獲取部署 URL

部署完成後，Railway 會給你一個 URL：
```
https://tcg-price-api-production.up.railway.app
```

---

### 方法 2：手動部署（無 GitHub）

如果不想用 GitHub，可以：

1. 訪問：https://railway.app
2. 登入後點擊 **"New Project"**
3. 選擇 **"Empty Service"**
4. 在 **"Settings"** 中：
   - **Root Directory**: `backend`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. 在 **"Variables"** 中添加：
   ```
   GEMINI_API_KEY = 你的 API Key
   PORT = 8000
   ```
6. 點擊 **"Deploy"**

---

## 🔗 綁定自定義域名（api.ecoxlabs.com）

### 在 Railway 設置

1. 進入你的 Railway 項目
2. 點擊 **"Settings"**
3. 找到 **"Domains"**
4. 點擊 **"Add Custom Domain"**
5. 輸入：`api.ecoxlabs.com`
6. Railway 會顯示 DNS 記錄

### 在 Dynadot 添加 DNS

返回 Dynadot DNS 設置，添加：

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

應該能看到 TCG Price Scanner 頁面！

---

## 🎯 快速檢查清單

- [ ] 後端部署到 Railway
- [ ] 設置 `GEMINI_API_KEY` 環境變量
- [ ] 獲取 Railway 部署 URL
- [ ] 綁定 `api.ecoxlabs.com` 域名
- [ ] 在 Dynadot 添加 API DNS 記錄
- [ ] 更新 Vercel `VITE_API_URL` 環境變量
- [ ] 測試完整功能

---

**完成每一步後告訴我，我會幫你檢查！** 🚀
