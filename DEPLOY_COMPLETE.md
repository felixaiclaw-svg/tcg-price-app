# ✅ TCG Price App - 部署完成報告

## 🎉 已完成

### ✅ 前端部署（Vercel）
- **狀態**: 已部署
- **URL**: https://frontend-five-indol-25.vercel.app
- **項目**: felixaiclaw-svgs-projects/frontend
- **構建**: 成功（187.99 kB）

---

## ⚠️ 需要完成的步驟

### 1️⃣ 綁定域名到 Vercel（www.ecoxlabs.com）

**在 Vercel Dashboard 操作：**

1. 訪問：https://vercel.com/felixaiclaw-svgs-projects/frontend/settings/domains
2. 點擊 **"Add"**
3. 輸入：`www.ecoxlabs.com`
4. 點擊 **"Add"**

**然後在 Dynadot 配置 DNS：**

1. 登入 Dynadot
2. 進入 `ecoxlabs.com` 的 DNS 管理
3. 添加以下記錄：

| 類型 | 名稱 | 目標 | TTL |
|------|------|------|-----|
| CNAME | www | cname.vercel-dns.com | 自動 |
| A | @ | 76.76.21.21 | 自動 |

**等待 DNS 生效**：通常 5-30 分鐘

---

### 2️⃣ 部署後端到 Railway

**網頁操作（最簡單）：**

1. 訪問：https://railway.app
2. 用 GitHub 登入
3. 點擊 **"New Project"**
4. 選擇 **"Deploy from GitHub repo"**
5. 選擇你的 repo（或上傳代碼）

**或者手動上傳：**

1. 訪問：https://railway.app
2. 點擊 **"New Project"** → **"Empty Service"**
3. 在 **"Settings"** 中找到 **"Root Directory"**，設置為 `backend`
4. 在 **"Variables"** 中添加：
   ```
   GEMINI_API_KEY = 你的 Gemini API Key（從 tcg-price-app/backend/.env 複製）
   PORT = 8000
   ```
5. 點擊 **"Deploy"**

**部署完成後：**
- Railway 會給你一個 URL，例如：`https://tcg-price-api-production.up.railway.app`
- 複製這個 URL

---

### 3️⃣ 更新前端 API 地址

**在 Vercel 設置環境變量：**

1. 訪問：https://vercel.com/felixaiclaw-svgs-projects/frontend/settings/environment-variables
2. 點擊 **"Add"**
3. 添加：
   - Key: `VITE_API_URL`
   - Value: `https://你的-railway-url.up.railway.app`
4. 點擊 **"Save"**
5. 重新部署前端（Vercel 會自動檢測並重新部署）

---

### 4️⃣ 綁定後端域名（api.ecoxlabs.com）

**在 Railway：**

1. 進入你的項目
2. 點擊 **"Settings"**
3. 找到 **"Domains"**
4. 點擊 **"Add Custom Domain"**
5. 輸入：`api.ecoxlabs.com`

**在 Dynadot DNS：**

添加記錄：
| 類型 | 名稱 | 目標 | TTL |
|------|------|------|-----|
| CNAME | api | 你的-railway-url.up.railway.app | 自動 |

---

## 🚀 快速測試

### 本地測試（立即可用）

前端和後端都在本地運行：
- 前端：http://localhost:3000
- 後端：http://localhost:8000

**啟動命令：**

```powershell
# 後端
cd C:\Users\felix\.openclaw\workspace\tcg-price-app\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端（新窗口）
cd C:\Users\felix\.openclaw\workspace\tcg-price-app\frontend
npm run dev
```

---

## 📦 自動化 Skills 安裝

讓我幫你安裝自動化相關的 skills：

```powershell
# GitHub 自動化
npx clawhub@latest install github --force

# 安全審查
npx clawhub@latest install skill-vetter --force

# MCP 工具管理
npx clawhub@latest install mcporter --force
```

---

## ✅ 完成後訪問

- **前端**: https://www.ecoxlabs.com
- **API**: https://api.ecoxlabs.com
- **API 文檔**: https://api.ecoxlabs.com/docs

---

## 📞 需要幫助？

完成每一步後告訴我，我會幫你檢查和繼續下一步！
