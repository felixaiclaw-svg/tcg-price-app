# TCG Price Scanner - 安裝指南

## 📋 系統要求

- **Python**: 3.9+
- **Node.js**: 18+
- **Tesseract OCR**: 需要安裝

---

## 🔧 後端設置 (Python FastAPI)

### 1. 安裝 Python 依賴

```bash
cd backend
pip install -r requirements.txt
```

### 2. 安裝 Tesseract OCR

**Windows:**
```bash
# 下載安裝程式
https://github.com/UB-Mannheim/tesseract/wiki

# 安裝後將 Tesseract 加入 PATH
# 或在代碼中指定路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 3. 啟動後端服務

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

訪問：http://localhost:8000/docs (API 文檔)

---

## 🌐 前端設置 (React + Vite)

### 1. 安裝 Node 依賴

```bash
cd frontend
npm install
```

### 2. 啟動開發服務器

```bash
npm run dev
```

訪問：http://localhost:3000

---

## 📱 移動端設置 (React Native)

### 1. 安裝 Expo CLI

```bash
npm install -g expo-cli
```

### 2. 創建移動端項目

```bash
npx create-expo-app mobile
cd mobile
npm install axios expo-camera expo-image-picker
```

### 3. 啟動移動應用

```bash
npx expo start
```

---

## 🚀 快速測試

### 測試 API

```bash
# 健康檢查
curl http://localhost:8000/api/v1/health

# 測試貨幣轉換
curl -X POST http://localhost:8000/api/v1/currency/convert \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currencies": ["MOP", "HKD", "RMB"]}'
```

### 測試網頁

1. 啟動後端：`http://localhost:8000`
2. 啟動前端：`http://localhost:3000`
3. 上傳卡牌圖片
4. 查看價格結果

---

## ⚙️ 配置說明

### 後端配置 (.env)

```env
# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# OCR 配置
TESSERACT_PATH=/usr/bin/tesseract

# 匯率 API (可選)
EXCHANGE_RATE_API_KEY=your_api_key

# Redis 快取 (可選)
REDIS_URL=redis://localhost:6379
```

### 前端配置

編輯 `frontend/src/App.tsx` 中的 `API_URL`:

```typescript
const API_URL = 'http://localhost:8000/api/v1';
// 生產環境改為實際服務器地址
// const API_URL = 'https://your-api.com/api/v1';
```

---

## 🐛 常見問題

### 1. Tesseract 無法識別

**問題**: OCR 無法識別文字

**解決**:
- 確保 Tesseract 正確安裝
- 檢查圖片質量 (建議 300dpi 以上)
- 調整圖片預處理參數

### 2. 爬蟲無法獲取價格

**問題**: 網站結構變更導致爬蟲失敗

**解決**:
- 更新 BeautifulSoup 選擇器
- 考慮使用官方 API (如有)
- 添加 Selenium 處理 JavaScript 渲染

### 3. CORS 錯誤

**問題**: 前端無法訪問後端 API

**解決**:
- 確保後端 CORS 設置正確
- 檢查前端代理配置

---

## 📦 生產部署

### Docker 部署

```bash
# 構建鏡像
docker build -t tcg-price-scanner .

# 運行容器
docker run -p 8000:8000 tcg-price-scanner
```

### 雲端部署

**推薦平台**:
- **Vercel** - 前端
- **Railway** - 後端
- **AWS/GCP** - 完整部署

---

## 📞 技術支援

如有問題，請查看:
- API 文檔：http://localhost:8000/docs
- 日誌文件：backend/logs/
- 錯誤報告：GitHub Issues

---

**祝使用愉快！** 🃏✨
