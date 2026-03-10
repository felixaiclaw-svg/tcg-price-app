# 🔐 安全部署指南

## 架構概述

```
┌─────────────────┐         ┌──────────────────┐
│  GitHub Pages   │ ──────▶ │    Railway       │
│   (前端靜態)     │  API    │  (後端 FastAPI)   │
│   HTTPS 自動     │ 請求    │   HTTPS 自動      │
└─────────────────┘         └──────────────────┘
```

## 為什麼這個方案最安全？

| 平台 | 安全特性 |
|------|----------|
| **GitHub Pages** | 自動 HTTPS、DDoS 保護、無服務器攻擊面 |
| **Railway** | 自動安全更新、隔離容器、自動 HTTPS |

✅ 無需管理服務器  
✅ 無需配置防火牆  
✅ 自動 SSL 證書  
✅ 免費層足夠使用  

---

## 📋 部署步驟

### 步驟 1：部署後端到 Railway

1. 訪問 [railway.app](https://railway.app)
2. 用 GitHub 賬號登錄
3. 點擊 **New Project** → **Deploy from GitHub repo**
4. 選擇 `tcg-price-app` 倉庫
5. Railway 會自動檢測 `backend/` 目錄（因為 `nixpacks.toml` 指定了 `root = "backend"`）
6. 等待部署完成

#### 設置環境變量（在 Railway Dashboard）

在 Railway 項目設置中添加：

```
HOST=0.0.0.0
PORT=8000
```

如果有 API 密鑰（如 Google Generative AI），也在此添加。

#### 獲取後端 URL

部署完成後，Railway 會給你一個 URL，格式類似：
```
https://tcg-price-app-production-xxxx.up.railway.app
```

**複製這個 URL**，下一步要用。

---

### 步驟 2：配置 GitHub Pages

#### 2.1 啟用 GitHub Pages

1. 進入你的 GitHub 倉庫頁面
2. 點擊 **Settings** → **Pages**
3. 在 **Source** 下選擇 **GitHub Actions**（不是 Branch）
4. 保存

#### 2.2 設置 API URL 變量

1. 進入倉庫 **Settings** → **Variables** → **Actions**
2. 點擊 **New repository variable**
3. 添加：
   - Name: `VITE_API_URL`
   - Value: 你在步驟 1 獲取的 Railway URL（例如 `https://xxx.up.railway.app`）

#### 2.3 觸發部署

1. 進入倉庫 **Actions** 標籤
2. 點擊左側的 **Deploy to GitHub Pages**
3. 點擊 **Run workflow** → **Run workflow**
4. 等待綠色對勾表示部署成功

#### 2.4 獲取前端 URL

部署完成後，你的前端 URL 是：
```
https://你的 GitHub 用戶名.github.io/tcg-price-app/
```

---

## 🔒 安全檢查清單

- [ ] Railway 後端 URL 只允許來自你的 GitHub Pages 域名的請求（可選 CORS 配置）
- [ ] 不要在 GitHub 倉庫中提交 `.env` 文件或 API 密鑰
- [ ] 定期更新依賴（`npm audit` 和 `pip check`）
- [ ] 啟用 Railway 的自動部署（默認已啟用）

---

## 🛠️ 後續維護

### 更新前端代碼
```bash
git add .
git commit -m "feat: 更新前端"
git push
# GitHub Actions 會自動部署到 Pages
```

### 更新後端代碼
```bash
git add .
git commit -m "feat: 更新後端"
git push
# Railway 會自動重新部署
```

### 查看部署日誌

- **GitHub Pages**: 倉庫 → Actions → 選擇 workflow
- **Railway**: Railway Dashboard → 項目 → Deployments

---

## 📞 常見問題

### Q: GitHub Pages 顯示 404
A: 確保：
1. GitHub Pages 源設置為 **GitHub Actions**
2. Workflow 運行成功（綠色對勾）
3. 訪問的 URL 包含倉庫名稱：`username.github.io/tcg-price-app/`

### Q: 前端無法連接後端
A: 檢查：
1. Railway 部署是否成功
2. `VITE_API_URL` 變量是否正確設置
3. 後端是否允許 CORS（檢查 `backend/app/main.py`）

### Q: Railway 部署失敗
A: 檢查：
1. `requirements.txt` 是否完整
2. `backend/app/main.py` 是否能正常運行
3. Railway 日誌中的錯誤信息

---

## 🌐 最終訪問地址

- **前端**: `https://<你的用戶名>.github.io/tcg-price-app/`
- **後端 API**: `https://<railway-app-name>.up.railway.app`

**完成！** 🎉
