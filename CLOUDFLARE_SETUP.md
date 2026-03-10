# 🔐 Cloudflare Tunnel 安全設置指南

**更新日期**: 2026-03-10 11:38  
**狀態**: cloudflared 已安裝 ✅

---

## ✅ 已完成

- ✅ cloudflared 已安裝
- ✅ 版本：2025.8.1
- ✅ 位置：C:\Program Files\cloudflared.exe

---

## 🔐 安全設置步驟

### ⚠️ 重要：需要 Cloudflare 賬戶

Cloudflare Tunnel **需要**你有 Cloudflare 賬戶和域名。

#### 如果已有 Cloudflare 賬戶

**步驟 1: 登錄 Cloudflare**
```bash
cloudflared tunnel login
```

會打開瀏覽器讓你登錄。

**步驟 2: 創建 Tunnel**
```bash
cloudflared tunnel create tcg-app
```

**步驟 3: 配置 Tunnel**

創建檔案：`%USERPROFILE%\.cloudflared\tunnel.yml`

```yaml
tunnel: tcg-app
credentials-file: C:\Users\你的用戶\.cloudflared\<tunnel-id>.json

ingress:
  - hostname: tcg.你的域名.com
    service: http://localhost:3000
  - service: http_status:404
```

**步驟 4: 運行 Tunnel**
```bash
cloudflared tunnel run tcg-app
```

---

### 🆓 如果沒有 Cloudflare 賬戶

**選項 A: 註冊免費 Cloudflare**

1. 訪問：https://dash.cloudflare.com/sign-up
2. 註冊免費賬戶
3. 添加域名（需要有自己的域名）
4. 按照上述步驟設置

**選項 B: 使用 ngrok（無需域名）**

如果不想買域名，可以用 ngrok：

```bash
# 安裝 ngrok
choco install ngrok

# 註冊免費賬戶（獲取 token）
# https://dashboard.ngrok.com/signup

# 連接賬戶
ngrok config add-authtoken 你的 token

# 運行（帶密碼保護）
ngrok http 3000 -basic-auth "admin:你的密碼"
```

---

## 🔒 安全加固措施

### 1. 基本認證（必須）

**ngrok**:
```bash
ngrok http 3000 -basic-auth "admin:強密碼123!"
```

**Cloudflare**:
在 Cloudflare Dashboard 設置 Access Policy：
- 需要郵件驗證
- 或需要特定郵箱才能訪問

### 2. HTTPS（自動）

- ✅ ngrok 自動提供 HTTPS
- ✅ Cloudflare 自動提供 HTTPS

### 3. 訪問日誌

**Cloudflare**:
```bash
cloudflared tunnel --logfile C:\logs\tunnel.log run tcg-app
```

### 4. 限制訪問 IP

**Cloudflare Dashboard** → WAF → Rules:
```
Allow only: 你的 IP
Block all others
```

---

## 💰 費用比較

| 服務 | 費用 | 需要域名 | 安全性 |
|------|------|---------|-------|
| **Cloudflare Tunnel** | $0 | ✅ 是 | 🟢 高 |
| **ngrok 免費版** | $0 | ❌ 否 | 🟡 中 |
| **ngrok Pro** | $8/月 | ❌ 否 | 🟢 高 |
| **局域網** | $0 | ❌ 否 | 🟢 最高 |

---

## 🎯 我的建議

### 最佳方案：局域網 + 偶爾 ngrok

**原因**:
1. ✅ 最安全（不外露）
2. ✅ 零費用
3. ✅ 夠用（手機 + 電腦）

**使用方式**:
- 在家：用局域網 (192.168.31.236:3000)
- 外出臨時需要：啟動 ngrok（用完即關）

---

## 📋 快速測試（ngrok 無需域名）

如果你想立即測試外網訪問：

### 步驟 1: 安裝 ngrok
```bash
choco install ngrok
```

### 步驟 2: 註冊免費賬戶
訪問：https://dashboard.ngrok.com/signup

### 步驟 3: 獲取 Token
登錄後複製你的 auth token

### 步驟 4: 連接賬戶
```bash
ngrok config add-authtoken 你的 token
```

### 步驟 5: 運行（帶密碼）
```bash
ngrok http 3000 -basic-auth "admin:強密碼"
```

會得到一個 URL：`https://xxxx.ngrok.io`

---

## ⚠️ 安全警告

使用內網穿透時：

1. ✅ **必須設置密碼**
2. ✅ **使用 HTTPS**
3. ✅ **不用時立即關閉**
4. ✅ **定期更換密碼**
5. ❌ **不要暴露敏感服務**

---

## 🚀 立即行動

### 選項 A: 局域網（推薦）

繼續使用：http://192.168.31.236:3000

### 選項 B: ngrok 快速測試

```bash
choco install ngrok
ngrok http 3000 -basic-auth "admin:你的密碼"
```

### 選項 C: Cloudflare Tunnel（需要域名）

需要你有 Cloudflare 賬戶和域名。

---

**建議先用局域網，真的需要外網再用 ngrok 臨時測試！** 🔐
