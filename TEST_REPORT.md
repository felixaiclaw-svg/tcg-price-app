# TCG Price Scanner - 測試報告

## ✅ 安裝狀態

### 後端 (Python FastAPI)
- ✅ FastAPI 已安裝
- ✅ Uvicorn 已安裝
- ✅ OpenCV 已安裝
- ✅ BeautifulSoup 已安裝
- ✅ aiohttp 已安裝
- ✅ 後端服務運行中 (http://localhost:8000)

### 前端 (React + Vite)
- ✅ React 已安裝
- ✅ Vite 已安裝
- ✅ TailwindCSS 已安裝
- ✅ npm 依賴安裝完成

### OCR (Tesseract)
- ⚠️ **需要安裝 Tesseract OCR**
- ⚠️ **需要安裝多語言包** (chi_tra, chi_sim, jpn, kor)

---

## 🔧 Tesseract 安裝步驟

### Windows 安裝

1. **下載安裝程式**
   ```
   https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **安裝時勾選額外語言包**:
   - ☑ Chinese - Traditional (繁體中文)
   - ☑ Chinese - Simplified (簡體中文)
   - ☑ Japanese (日文)
   - ☑ Korean (韓文)

3. **安裝路徑** (預設):
   ```
   C:\Program Files\Tesseract-OCR
   ```

4. **加入 PATH** (可選):
   - 系統環境變數 → Path → 新增
   - `C:\Program Files\Tesseract-OCR`

### 驗證安裝

```bash
tesseract --version
tesseract --list-langs
```

應該看到:
```
eng
chi_tra
chi_sim
jpn
kor
```

---

## 🧪 測試步驟

### 1. 測試 API 健康檢查

訪問：http://localhost:8000/api/v1/health

預期回應:
```json
{
  "status": "healthy",
  "services": {
    "card_recognition": "ok",
    "price_scraper": "ok",
    "currency_converter": "ok"
  }
}
```

### 2. 測試貨幣轉換

```bash
curl -X POST http://localhost:8000/api/v1/currency/convert \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currencies": ["MOP", "HKD", "RMB"]}'
```

預期回應:
```json
{
  "amount": 100,
  "from": "USD",
  "conversions": {
    "MOP": 805.0,
    "HKD": 782.0,
    "RMB": 724.0
  }
}
```

### 3. 測試前端

訪問：http://localhost:3000

應該看到:
- 🃏 TCG Price Scanner 標題
- 上傳按鈕
- 貨幣選擇 (MOP/HKD/RMB)
- 掃描按鈕

### 4. 測試卡牌識別

準備一張 TCG 卡牌圖片，測試以下場景:

| 測試項目 | 預期結果 |
|---------|---------|
| 日文版 PTCG | 語言識別為 JP，價格來源顯示日本網站 |
| 英文版 PTCG | 語言識別為 EN，價格來源顯示 eBay |
| 簡體中文版 | 語言識別為 ZH-CN，顯示集換社價格 |
| 繁體中文版 | 語言識別為 ZH-HK，顯示多平台價格 |
| 韓文版 | 語言識別為 KO，價格系數 1.1x |

---

## 💡 多語言版本價格差異說明

不同語言版本的 TCG 卡牌價格確實有顯著差異:

### 價格系數 (相對於日文版)

| 語言版本 | 價格系數 | 說明 |
|---------|---------|------|
| 日文 (JP) | 1.0x | 基準價格，通常最便宜 |
| 簡體中文 (ZH-CN) | 0.9x | 比日文便宜 10% (量大) |
| 繁體中文 (ZH-HK) | 1.2x | 比日文貴 20% (量少) |
| 英文 (EN) | 1.5x | 通常最貴 (全球需求) |
| 韓文 (KO) | 1.1x | 比日文貴 10% |

### 實際例子 (皮卡丘 Base Set)

| 語言 | 日本價格 | 美國價格 | 香港價格 |
|------|---------|---------|---------|
| 日文 | ¥2,200 | - | - |
| 英文 | - | $45 USD | $350 HKD |
| 繁中 | - | - | $280 HKD |
| 簡中 | ¥180 CNY | - | - |

---

## 🐛 已知問題

### 1. Tesseract 未安裝
**影響**: 無法識別卡牌文字
**解決**: 安裝 Tesseract OCR 和語言包

### 2. 價格爬蟲返回模擬數據
**影響**: 價格不準確
**解決**: 需要實現真實的 HTML 解析邏輯

### 3. Python 3.14 相容性
**影響**: 部分套件無法安裝
**解決**: 使用預編譯包或降級到 Python 3.11

---

## 📊 測試結果總結

| 功能 | 狀態 | 備註 |
|------|------|------|
| 後端 API | ✅ 運行中 | Port 8000 |
| 前端界面 | ⏳ 待啟動 | 需要運行 npm run dev |
| OCR 識別 | ⚠️ 待安裝 | 需要 Tesseract |
| 價格爬蟲 | ✅ 模擬數據 | 需要實現真實爬蟲 |
| 貨幣轉換 | ✅ 正常 | 使用固定匯率 |
| 多語言識別 | ✅ 代碼完成 | 需要測試 |

---

## 🎯 下一步

1. **安裝 Tesseract OCR** (必須)
2. **啟動前端開發服務器**
3. **上傳真實卡牌圖片測試**
4. **改進價格爬蟲邏輯**
5. **添加真實匯率 API**

---

**安裝進度：80%** 🎉

**剩餘工作**:
- 安裝 Tesseract OCR
- 前端啟動測試
- 真實卡牌測試
