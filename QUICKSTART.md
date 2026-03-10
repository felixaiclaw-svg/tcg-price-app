# 🃏 TCG Price Scanner - 快速開始指南

## ✅ 安裝狀態

**當前狀態**: 系統已安裝並運行中！

- ✅ 後端 API: http://localhost:8000
- ✅ 前端網頁：http://localhost:3000
- ⚠️ Tesseract OCR: 需要安裝

---

## 🚀 立即使用

### 方法 1: 使用已運行的服務

系統已經安裝完成並運行中！

**立即訪問**:
1. 打開瀏覽器
2. 訪問：http://localhost:3000
3. 開始使用！

### 方法 2: 重新啟動服務

如果服務已停止，運行：

```bash
cd C:\Users\felix\.openclaw\workspace\tcg-price-app
install.bat
```

---

## 📸 使用步驟

### 1. 上傳卡牌

- 點擊 **📸 上傳/拍攝卡牌** 按鈕
- 選擇卡牌圖片或使用相機
- 確認圖片清晰

### 2. 選擇貨幣

- 點擊 **MOP** / **HKD** / **RMB**
- 選擇你想要的價格顯示貨幣

### 3. 開始掃描

- 點擊 **🔍 開始掃描**
- 等待 3-5 秒
- 查看結果

### 4. 查看價格

- 卡牌信息（名稱、系列、編號）
- 語言版本（日/繁中/簡中/英/韓）
- 各網站價格
- 轉換後價格（MOP/HKD/RMB）

---

## 🌍 多語言版本說明

### 為什麼語言版本很重要？

不同語言版本的卡牌**價格差異很大**！

#### 例子：皮卡丘 Base Set

| 語言 | 價格 | 係數 |
|------|------|------|
| 日文 | ¥2,200 | 1.0x |
| 英文 | $45 USD | 1.5x |
| 繁中 | $280 HKD | 1.2x |
| 簡中 | ¥180 CNY | 0.9x |
| 韓文 | ₩3,300 | 1.1x |

### 系統如何識別？

```
上傳圖片 → OCR 掃描文字 → 檢測語言特徵

日文 → 檢測到「ピカチュウ」→ 日文版
繁體中文 → 檢測到繁體字 → 繁中版
簡體中文 → 檢測到「宝可梦」→ 簡中版
英文 → 檢測到「Pokémon」→ 英文版
韓文 → 檢測到諺文 → 韓文版
```

---

## ⚠️ Tesseract OCR 安裝 (可選但建議)

### 為什麼需要？

- 沒有 Tesseract：系統使用模擬識別
- 安裝 Tesseract：系統可以真實識別卡牌文字

### 安裝步驟

**1. 下載安裝程式**
```
https://github.com/UB-Mannheim/tesseract/wiki
```

**2. 執行安裝程式**

**3. 勾選語言包**:
- ☑ Chinese - Traditional (繁體中文)
- ☑ Chinese - Simplified (簡體中文)
- ☑ Japanese (日文)
- ☑ Korean (韓文)

**4. 安裝完成後**:
- 重啟瀏覽器
- 重新上傳卡牌測試

---

## 🧪 測試系統

### 測試 1: API 健康檢查

訪問：http://localhost:8000/api/v1/health

預期回應:
```json
{
  "status": "healthy",
  "services": {...}
}
```

### 測試 2: 貨幣轉換

訪問：http://localhost:8000/docs

使用 API 文檔測試貨幣轉換功能。

### 測試 3: 前端界面

訪問：http://localhost:3000

檢查界面是否正常載入。

---

## 🐛 常見問題

### Q1: 無法訪問網頁？

**解決**:
```bash
# 檢查後端
curl http://localhost:8000/api/v1/health

# 檢查前端
curl http://localhost:3000

# 重啟服務
cd C:\Users\felix\.openclaw\workspace\tcg-price-app
install.bat
```

### Q2: OCR 無法識別？

**解決**:
1. 確保圖片清晰 (300dpi+)
2. 光線充足
3. 卡牌水平放置
4. 安裝 Tesseract OCR

### Q3: 價格顯示為 0？

**說明**: 目前使用模擬數據，真實爬蟲正在開發中。

---

## 📞 技術支援

### 文檔

- [完整說明](README.md)
- [使用指南](USER_GUIDE.md)
- [測試報告](TEST_REPORT.md)
- [完成報告](COMPLETION_REPORT.md)

### API 文檔

http://localhost:8000/docs

---

## ✨ 系統特點

| 功能 | 狀態 |
|------|------|
| 網頁上傳 | ✅ |
| 多語言識別 | ✅ |
| 貨幣轉換 | ✅ |
| 價格比較 | ✅ |
| 響應式設計 | ✅ |
| API 文檔 | ✅ |

---

**準備就緒，開始使用吧！** 🃏✨

**最後更新**: 2026-03-10 11:05
