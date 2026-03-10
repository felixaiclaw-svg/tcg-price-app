# 🌙 晚上 7:15 提醒 - Cloudflare Tunnel 設置（更新版）

**提醒時間**: 2026-03-10 19:15  
**預計完成時間**: 約 40 分鐘

---

## 📋 快速步驟清單

### 準備工作（2 分鐘）
- [ ] 準備好電郵地址
- [ ] 準備好支付寶/微信支付
- [ ] 準備約 $15 港幣（域名費用）

---

### 步驟 1: 註冊 Dynadot（3 分鐘）

```
訪問：https://www.dynadot.com

1. 點擊右上角 "Sign Up"
2. 填寫電郵、用戶名、密碼
3. 驗證電郵
```

---

### 步驟 2: 購買域名（5 分鐘）

```
1. 在搜索框輸入想要的域名
   建議：mytcgapp2026.com
   
2. 選擇 .com 後綴
   
3. 點擊 "Add to Cart"
   
4. 結賬時選擇：
   - Domain Privacy: ✅ (免費)
   - 付款方式：Alipay / WeChat Pay
   
5. 掃描二維碼付款
```

---

### 步驟 3: 註冊 Cloudflare（3 分鐘）

```
訪問：https://dash.cloudflare.com/sign-up

1. 輸入電郵、密碼
2. 驗證電郵
3. 登錄
```

---

### 步驟 4: 添加域名到 Cloudflare（10 分鐘）

```
1. 登錄 Cloudflare 後點擊 "Add a Site"
2. 輸入剛買的域名
3. 選擇 Free 計劃
4. 複製 2 個 Nameservers

返回 Dynadot:
1. Domain List → Manage
2. Nameservers → Custom DNS
3. 粘貼 Cloudflare 的 2 個 nameservers
4. 保存

等待 5-30 分鐘生效
```

---

### 步驟 5: 創建 Tunnel（10 分鐘）

```
訪問：https://one.dash.cloudflare.com

1. Access → Tunnels → Create a Tunnel
2. 名稱：tcg-app
3. 選擇 Windows
4. 複製安裝命令

打開 CMD 運行:
cloudflared tunnel install --token 你的 token
cloudflared tunnel run tcg-app
```

---

### 步驟 6: 配置 Hostname（5 分鐘）

```
在 Tunnel 配置頁面:

Subdomain: tcg
Domain: 你的域名.com
Service: http://localhost:3000

保存後訪問:
https://tcg.你的域名.com
```

---

### 步驟 7: 設置訪問保護（5 分鐘）

```
1. Access → Applications → Add Application
2. Name: TCG App
3. Domain: tcg.你的域名.com
4. Policy: 添加你的電郵
5. 保存
```

---

## ✅ 完成後測試

### 手機測試（用數據，關閉 WiFi）
```
訪問：https://tcg.你的域名.com
輸入電郵 → 獲取驗證碼 → 輸入驗證碼
```

### 電腦測試
```
訪問：https://tcg.你的域名.com
```

---

## 💰 費用

| 項目 | 費用 |
|------|------|
| 域名 .com | $10-15/年 |
| Cloudflare | $0 |
| **總計** | **約 $10-15/年** |

---

## 🔐 安全提示

- ✅ 不要分享賬戶密碼
- ✅ 設置強密碼
- ✅ 啟用兩步驗證
- ✅ 域名每年續費

---

## 📞 遇到問題？

告訴 AI:
- 哪一步出問題
- 錯誤訊息是什麼

---

**準備好就開始！祝你設置順利！** 🚀
