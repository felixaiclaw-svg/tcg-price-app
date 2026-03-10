# 🔐 ngrok 安全使用指南

**更新日期**: 2026-03-10 11:45  
**狀態**: ngrok 已安裝 ✅

---

## ✅ ngrok 已安裝

- ✅ 版本：3.3.1
- ✅ 位置：C:\Users\felix\AppData\Local\Programs\ngrok
- ✅ 命令：ngrok

---

## 🔒 安全性評估

### ngrok 安全性：🟡 中等（有保護措施）

| 安全措施 | 狀態 | 說明 |
|---------|------|------|
| **HTTPS 加密** | ✅ | 自動提供 |
| **基本認證** | ✅ | 用戶名 + 密碼 |
| **隨機 URL** | ✅ | 每次重啟都變 |
| **臨時使用** | ✅ | 用完即關 |

### ⚠️ 安全警告

**ngrok 適合**:
- ✅ 臨時外網訪問
- ✅ 個人測試使用
- ✅ 短期分享

**ngrok 不適合**:
- ❌ 長期 24/7 運行
- ❌ 敏感數據傳輸
- ❌ 公開服務

---

## 🚀 首次設置（5 分鐘）

### 步驟 1: 註冊 ngrok 賬戶

訪問：https://dashboard.ngrok.com/signup

1. 輸入電郵
2. 設置密碼
3. 驗證電郵
4. 登錄

### 步驟 2: 獲取 Authtoken

1. 登錄後訪問：https://dashboard.ngrok.com/get-started/your-authtoken
2. 複製你的 token（長長的字串）

### 步驟 3: 配置 ngrok

打開命令提示字元（CMD）：

```bash
ngrok config add-authtoken 你的 token
```

例如：
```bash
ngrok config add-authtoken 2aBcDeFgHiJkLmNoPqRsTuVwXyZ123456789
```

看到 `Authtoken saved` 表示成功！

---

## 📱 使用 ngrok（兩種方法）

### 方法 1: 使用啟動腳本（推薦）

**運行**:
```
start-ngrok.bat
```

**會顯示**:
```
Forwarding: https://xxxx-xxxx.ngrok.io -> http://localhost:3000
```

**訪問**:
- 手機/外網：https://xxxx-xxxx.ngrok.io
- 用戶名：`admin`
- 密碼：`TCG2026!@#`

### 方法 2: 手動啟動

```bash
ngrok http 3000 -basic-auth "admin:你的密碼"
```

---

## 🔐 自定義密碼

編輯 `start-ngrok.bat`，修改這兩行：

```batch
set NGROK_USER=你的用戶名
set NGROK_PASS=你的強密碼
```

**密碼建議**:
- ✅ 至少 8 個字符
- ✅ 包含大小寫
- ✅ 包含數字和符號
- ❌ 不要用簡單密碼

---

## 📊 使用流程

```
1. 需要外網訪問
   ↓
2. 運行 start-ngrok.bat
   ↓
3. 複製顯示的 URL（https://xxxx.ngrok.io）
   ↓
4. 手機/外網訪問 + 輸入密碼
   ↓
5. 用完關閉窗口
```

---

## ⚠️ 重要安全提示

### ✅ 必須做的

1. **設置強密碼**
   - 不要用預設密碼
   - 定期更換

2. **不要分享 URL**
   - 只自己使用
   - 如果必須分享，用完立即關閉

3. **用完即關**
   - 不要長期運行
   - 關閉 ngrok 窗口

4. **監控訪問**
   - 查看 ngrok 窗口日誌
   - 注意異常訪問

### ❌ 不要做的

1. ❌ 不要 24/7 運行
2. ❌ 不要分享給陌生人
3. ❌ 不要傳輸敏感數據
4. ❌ 不要暴露其他服務

---

## 💰 費用說明

### ngrok 免費版

| 項目 | 限制 |
|------|------|
| **費用** | $0 |
| **流量** | 40GB/月 |
| **連接數** | 5 個/分鐘 |
| **URL** | 隨機（每次變） |
| **HTTPS** | ✅ 包含 |
| **基本認證** | ✅ 包含 |

### ngrok Pro（如需升級）

| 項目 | 價格 |
|------|------|
| **費用** | $8/月 |
| **流量** | 無限 |
| **自定義域名** | ✅ |
| **更高限額** | ✅ |

---

## 🎯 使用場景

### ✅ 適合

- 在外面想訪問家裡電腦
- 臨時給朋友展示
- 測試外網訪問
- 短期項目演示

### ❌ 不適合

- 長期對外服務
- 電商網站
- 敏感數據系統
- 需要高可用性

---

## 📋 快速參考

### 啟動 ngrok
```bash
# 方法 1: 使用腳本
start-ngrok.bat

# 方法 2: 手動
ngrok http 3000 -basic-auth "admin:你的密碼"
```

### 查看狀態
- ngrok 窗口會顯示訪問日誌
- 在線 Dashboard: https://dashboard.ngrok.com

### 停止 ngrok
- 關閉 ngrok 窗口
- 或按 `Ctrl+C`

---

## 🐛 常見問題

### Q1: 無法連接？

**檢查**:
1. 網絡是否正常？
2. ngrok token 是否正確？
3. 端口 3000 是否被佔用？

**解決**:
```bash
# 檢查 ngrok 配置
ngrok config check

# 重新配置 token
ngrok config add-authtoken 新 token
```

### Q2: 速度很慢？

**原因**:
- 免費版限速
- 服務器距離遠

**解決**:
- 升級 Pro
- 或用局域網

### Q3: URL 每次都不一樣？

**正常現象**！這是安全特性。

如果需要固定 URL，需要：
- 升級 Pro ($8/月)
- 或用 Cloudflare Tunnel（需要域名）

---

## ✨ 總結

### ngrok 安全性：🟡 中等

**適合**: 臨時外網訪問  
**費用**: 免費（40GB/月）  
**安全**: 有密碼保護 + HTTPS  

### 使用建議

1. ✅ 設置強密碼
2. ✅ 用完即關
3. ✅ 不分享 URL
4. ✅ 定期更換密碼

---

**準備就緒！運行 `start-ngrok.bat` 開始使用！** 🔐🚀
