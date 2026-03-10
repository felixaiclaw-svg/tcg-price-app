# TCG Price App - 部署指南

## 快速部署（推薦）

### 1. 前端部署到 Cloudflare Pages

```powershell
# 執行部署腳本
cd C:\Users\felix\.openclaw\workspace\tcg-price-app
.\deploy-to-cloudflare.bat
```

**首次使用需要登入 Cloudflare：**
```powershell
wrangler login
```

### 2. 後端部署到 Railway

1. 訪問：https://railway.app
2. 註冊/登入（可用 GitHub 登入）
3. 點擊 **"New Project"**
4. 選擇 **"Deploy from GitHub repo"**
5. 選擇你的 repo 或上傳代碼
6. 設置環境變量：
   - `GEMINI_API_KEY`: 你的 Google Gemini API Key
   - `PORT`: 自動設置
7. 點擊 **"Deploy"**

部署完成後，Railway 會給你一個 URL，例如：
`https://tcg-price-api-production.up.railway.app`

### 3. 配置前端 API 地址

修改 `frontend/wrangler.toml`：
```toml
[vars]
VITE_API_URL = "https://你的-railway-url.up.railway.app"
```

然後重新部署前端：
```powershell
wrangler pages deploy dist --project-name=tcg-price-app
```

### 4. 綁定自定義域名 ecoxlabs.com

#### Cloudflare Pages:
1. 訪問：https://dash.cloudflare.com
2. 進入 **Workers & Pages** → 選擇 **tcg-price-app**
3. 點擊 **"Custom domains"**
4. 點擊 **"Add custom domain"**
5. 輸入：`www.ecoxlabs.com`
6. Cloudflare 會自動配置 DNS

#### Railway:
1. 進入你的 Railway 項目
2. 點擊 **"Settings"**
3. 找到 **"Domains"**
4. 添加：`api.ecoxlabs.com`

#### Dynadot DNS 設置:
1. 登入 Dynadot
2. 進入 **ecoxlabs.com** 的 DNS 管理
3. 添加記錄：
   ```
   類型：CNAME
   名稱：www
   目標：tcg-price-app.pages.dev
   
   類型：CNAME
   名稱：api
   目標：你的-railway-url.up.railway.app
   ```

---

## 本地測試

### 前端
```powershell
cd frontend
npm run dev
```
訪問：http://localhost:3000

### 後端
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 環境變量

### 後端 (.env)
```env
GEMINI_API_KEY=你的 Gemini API Key
PORT=8000
```

### 前端 (wrangler.toml)
```toml
[vars]
VITE_API_URL = "https://api.ecoxlabs.com"
```

---

## 完成後訪問

- 前端：https://www.ecoxlabs.com
- API: https://api.ecoxlabs.com
- API 文檔：https://api.ecoxlabs.com/docs
