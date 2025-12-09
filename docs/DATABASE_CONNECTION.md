# PostgreSQL 資料庫連線說明

## 重要：連線方式因執行環境而異

### 資料庫資訊
- **使用者**: agvc
- **密碼**: 36274806
- **端口**: 5432
- **資料庫**: AGVC、agvc

---

## ✅ 從 pgAdmin 連線（在 Docker 容器內）

**pgAdmin 登入**:
- 網址: http://localhost:5050
- Email: ct@ching-tech.com
- Password: 36274806

**連線到 PostgreSQL**:
- **Host name/address**: `192.168.100.254` ⚠️ **必須用 IP，不能用 localhost**
- **Port**: `5432`
- **Database**: `AGVC` 或 `agvc`
- **User**: `agvc`
- **Password**: `36274806`

**為什麼不能用 localhost？**
- pgAdmin 在 Docker 容器內運行
- 容器內的 localhost 指向 pgAdmin 自己，不是 PostgreSQL
- 必須使用 PostgreSQL 容器的內部 IP: `192.168.100.254`

---

## ✅ 從 Host 機器連線（Python 腳本、命令列）

**Python 範例** (db_init.py):
```python
DB_CONFIG = {
    'host': 'localhost',  # ⚠️ 在 host 上用 localhost
    'port': 5432,
    'user': 'agvc',
    'password': '36274806',
    'database': 'AGVC'
}
```

**命令列範例**:
```bash
# 在 host 機器上
psql -h localhost -p 5432 -U agvc -d AGVC
```

**為什麼用 localhost？**
- Python 腳本在 Windows host 機器上運行
- Docker 已將容器端口 5432 映射到 host 的 5432
- 所以用 localhost:5432 可以連到容器

---

## ❌ 常見錯誤

### 錯誤 1: 在 pgAdmin 中使用 localhost
```
❌ Host: localhost
✅ Host: 192.168.100.254
```
錯誤訊息: `Connection refused` 或 `getaddrinfo failed`

### 錯誤 2: 在 Python 腳本中使用容器 IP
```python
❌ 'host': '192.168.100.254'
✅ 'host': 'localhost'
```
錯誤訊息: `Connection timed out`

---

## 網路架構圖

```
┌─────────────────────────────────────┐
│     Windows Host 機器               │
│                                     │
│  Python 腳本 ──→ localhost:5432    │ ← 使用 localhost
│       ↓                             │
│  [Docker 端口映射]                  │
│       ↓                             │
└─────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────┐
│  Docker Network (192.168.100.0/24)  │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   pgAdmin    │  │  PostgreSQL │ │
│  │ .101:80      │→│  .254:5432  │ │ ← pgAdmin 使用 192.168.100.254
│  └──────────────┘  └─────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

---

## 快速參考

| 執行位置 | Host 設定 | 原因 |
|---------|----------|------|
| pgAdmin (容器內) | `192.168.100.254` | 容器間通訊用內部 IP |
| Python/CLI (host上) | `localhost` | 透過端口映射連接 |

---

## 在 pgAdmin 中註冊伺服器

### 為什麼要註冊伺服器？

pgAdmin 提供兩種連線方式：
1. **Query Tool 臨時連線**：只能執行 SQL，用完即丟，無法瀏覽資料庫結構
2. **註冊伺服器**：永久保存連線，可以圖形化管理資料庫、表格、索引等

### 註冊步驟

1. **右鍵點選左側 "Servers"** → **Register → Server...**

2. **General 標籤頁**：
   - Name: `AGVC Server`（或任何你喜歡的名稱）

3. **Connection 標籤頁**：
   - Host name/address: `192.168.100.254` ⚠️ **重要：必須用 IP**
   - Port: `5432`
   - Maintenance database: `postgres`
   - Username: `agvc`
   - Password: `36274806`
   - ✅ 勾選 **Save password**

4. 點擊 **Save**

### 註冊後的效果

左側會出現：
```
Servers
  └─ AGVC Server
      └─ Databases (2)
          ├─ agvc      ← docker-compose 建立
          └─ postgres  ← 系統預設
```

---

## 初始化與驗證

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 執行連線測試 (在 host 上)
```bash
python db_init.py
```

### 3. 驗證資料庫
```bash
docker exec postgres psql -U agvc -c "\l"
```

---

## 資料庫說明

| 資料庫 | 來源 | 用途 |
|--------|------|------|
| `postgres` | PostgreSQL 系統預設 | 系統資料庫，不可刪除 |
| `agvc` | docker-compose.yaml 中 `POSTGRES_DB` | 專案使用的主資料庫 |

---

## Windows 本地 pgAdmin 連線

如果你在 Windows 本地安裝了 pgAdmin（不是 Docker 容器內的 pgAdmin），可以這樣連線：

### 在 Windows 本地 pgAdmin 中註冊 Docker PostgreSQL

1. **開啟 Windows 本地的 pgAdmin**

2. **右鍵點選 "Servers"** → **Register → Server...**

3. **General 標籤頁**：
   - Name: `Docker PostgreSQL`

4. **Connection 標籤頁**：
   - Host name/address: `localhost` ⚠️ **用 localhost，不是 192.168.100.254**
   - Port: `5432`
   - Maintenance database: `postgres`
   - Username: `agvc`
   - Password: `36274806`
   - ✅ 勾選 Save password

5. 點擊 **Save**

### pgAdmin 連線對照表

| pgAdmin 位置 | Host 設定 | 原因 |
|-------------|----------|------|
| **Windows 本地 pgAdmin** | `localhost` | 透過 Docker 端口映射 |
| **Docker 容器 pgAdmin** (http://localhost:5050) | `192.168.100.254` | 容器間通訊 |

---

## 解決端口衝突（Windows 本地也有 PostgreSQL）

如果 Windows 本地也安裝了 PostgreSQL，可能會有端口衝突（都想用 5432）。

### 方案 1: 停用 Windows PostgreSQL 服務

1. 按 `Win + R` → 輸入 `services.msc`
2. 找到 `postgresql-x64-xx` 服務
3. 右鍵 → **停止**
4. 右鍵 → **內容** → 啟動類型改為 **手動** 或 **已停用**

### 方案 2: 修改 Windows PostgreSQL 端口（推薦）

這樣兩個 PostgreSQL 可以同時運行。

#### 步驟：

1. **以管理員身份開啟記事本**：
   - 在開始選單搜尋 "記事本"
   - 右鍵 → **以系統管理員身分執行**

2. **開啟配置檔**：
   ```
   C:\Program Files\PostgreSQL\18\data\postgresql.conf
   ```

3. **修改端口**（Ctrl+F 搜尋 "port"）：
   ```conf
   # 原本：
   #port = 5432

   # 改成：
   port = 5433
   ```

4. **儲存檔案**

5. **重啟 PostgreSQL 服務**：
   - 按 `Win + R` → 輸入 `services.msc`
   - 找到 `postgresql-x64-18` 服務
   - 右鍵 → **重新啟動**

#### 修改後的連線方式：

| PostgreSQL 位置 | Host | Port | 用途 |
|----------------|------|------|------|
| **Docker 容器** | `localhost` | `5432` | AGVC 專案使用 |
| **Windows 本地** | `localhost` | `5433` | 其他用途 |

這樣就不會衝突了！
