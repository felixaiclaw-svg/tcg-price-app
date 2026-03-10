# TCG Price Scanner 🃏

跨平台 TCG 卡牌價格查詢應用 - 支援網頁、iOS、Android

## 功能特點

- 📸 **拍照/上傳識別** - 支援 PTCG、OPCG 等 TCG 卡牌
- 🌍 **多語言支援** - 中/英/日/簡/韓版本卡牌識別
- 💰 **多平台價格** - eBay、snkrdunk、集換社、Mercari、yuyu-tei.jp
- 💱 **貨幣轉換** - MOP、HKD、RMB 自由轉換
- 📱 **跨平台** - Web、iOS、Android 一套代碼

## 技術棧

### 前端
- **React** + **TypeScript** - 網頁版
- **React Native** - iOS/Android
- **TailwindCSS** - 樣式

### 後端
- **Python FastAPI** - API 服務
- **OpenCV** + **Tesseract** - OCR 圖像識別
- **BeautifulSoup** + **Selenium** - 價格爬蟲
- **Redis** - 快取

### 第三方 API
- **Exchange Rate API** - 貨幣轉換
- **Image Recognition** - 卡牌識別

## 專案結構

```
tcg-price-app/
├── frontend/           # 網頁前端
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── backend/            # Python 後端
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── utils/
│   └── requirements.txt
├── mobile/             # React Native
│   └── App.tsx
└── scripts/            # 工具腳本
```

## 快速開始

### 後端啟動
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 前端啟動
```bash
cd frontend
npm install
npm run dev
```

### 移動端
```bash
cd mobile
npm install
npx expo start
```

## 支援卡牌系列

- ✅ Pokémon TCG (PTCG)
- ✅ One Piece Card Game (OPCG)
- ✅ Yu-Gi-Oh!
- ✅ Magic: The Gathering
- ✅ 遊戲王

## 價格來源

| 網站 | 地區 | 貨幣 |
|------|------|------|
| eBay | 全球 | USD |
| snkrdunk | 日本 | JPY |
| 集換社 | 中國 | CNY |
| Mercari | 日本 | JPY |
| yuyu-tei.jp | 日本 | JPY |

## License

MIT License
