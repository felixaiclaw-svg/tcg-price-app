# 🚀 Railway 部署 - 最終簡化版

## ✅ 已完成

- [x] GitHub Pages 已啟用
- [x] 前端部署 Workflow 已創建
- [x] Railway Token 已設置為 GitHub Secret

---

## ⚠️ 需要手動完成的步驟（只需一次，3 分鐘）

### 步驟 1：在 Railway 創建項目

1. 訪問：**https://railway.com**
2. 用 GitHub 賬號登錄
3. 點擊 **New Project**
4. 選擇 **Deploy from GitHub repo**
5. 選擇 `felixaiclaw-svg/tcg-price-app`
6. Railway 會自動檢測並部署 `backend/` 目錄
7. 等待部署完成（約 2-3 分鐘）

### 步驟 2：獲取後端 URL

1. 在 Railway Dashboard 點擊你的項目
2. 點擊 **Settings** 標籤
3. 找到 **Domains** 部分
4. 點擊 **Generate Domain**（如果還沒有的話）
5. 複製 URL（格式：`https://xxx.up.railway.app`）

### 步驟 3：更新 GitHub 環境變量

1. 訪問：**https://github.com/felixaiclaw-svg/tcg-price-app/settings/variables/actions**
2. 編輯 `VITE_API_URL`
3. 將值改為你的 Railway URL
4. 保存

### 步驟 4：重新觸發前端部署

1. 訪問：**https://github.com/felixaiclaw-svg/tcg-price-app/actions**
2. 點擊 **Deploy to GitHub Pages**
3. 點擊 **Run workflow**
4. 等待完成（綠色對勾）

---

## 🎉 完成！

| 組件 | URL |
|------|-----|
| 前端 | https://felixaiclaw-svg.github.io/tcg-price-app/ |
| 後端 | https://你的-app.up.railway.app |

---

## 📝 後續自動部署

完成後，每次 push 到 master 分支：
- **前端代碼變更** → 自動部署到 GitHub Pages
- **後端代碼變更** → Railway 會自動檢測並部署

---

## ❓ 需要幫助？

如果遇到問題，請告訴我具體哪一步出錯！
