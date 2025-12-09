# AGV API 使用指南

## 服務資訊

- **基礎 URL**: `http://localhost:8000`
- **API 版本**: v1
- **API 前綴**: `/api/v1`

## API 文檔

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 啟動與停止 API Server

### 啟動 Server

#### 方法 1：開發模式（推薦）
```bash
python -m uvicorn app.main:app --reload --port 8000
```
- `--reload`: 檔案修改時自動重新載入（開發時使用）
- `--port 8000`: 指定端口為 8000

#### 方法 2：指定 Host 和 Port
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- `--host 0.0.0.0`: 允許外部訪問（預設只允許 localhost）

#### 方法 3：生產模式
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
- `--workers 4`: 使用 4 個工作進程（根據 CPU 核心數調整）
- 不使用 `--reload`

### 停止 Server

#### 前台運行時
按 `Ctrl + C` 即可停止

#### 背景運行時（Windows）
```bash
# 1. 查找 Python 進程
tasklist | findstr "python"

# 2. 根據 PID 終止進程
taskkill /F /PID <PID>
```

#### 背景運行時（Linux/Mac）
```bash
# 1. 查找進程
ps aux | grep uvicorn

# 2. 終止進程
kill <PID>
```

### 檢查 Server 是否運行

#### 方法 1：訪問根路由
```bash
curl http://localhost:8000/
```

#### 方法 2：健康檢查端點
```bash
curl http://localhost:8000/health
```

**預期回應**:
```json
{
  "status": "healthy"
}
```

---

## AGV API 端點

### 1. 新增 AGV（INSERT）

**端點**: `POST /api/v1/agv/`

**請求範例**:
```json
{
  "name": "AGV01",
  "model": "K400",
  "description": "倉庫搬運車",
  "enable": 1
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/agv/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AGV01",
    "model": "K400",
    "description": "倉庫搬運車",
    "enable": 1
  }'
```

**回應**:
```json
{
  "id": 1,
  "name": "AGV01",
  "description": "倉庫搬運車",
  "model": "K400",
  "enable": 1,
  "created_at": "2025-12-05T14:00:00",
  "updated_at": "2025-12-05T14:00:00"
}
```

---

### 2. 查詢所有 AGV（GET ALL）

**端點**: `GET /api/v1/agv/`

**查詢參數**:
- `skip` (int): 跳過筆數，預設 0
- `limit` (int): 限制筆數，預設 100
- `enabled_only` (bool): 只查詢啟用的 AGV，預設 false

**請求範例**:
```bash
# 查詢所有 AGV
curl "http://localhost:8000/api/v1/agv/"

# 只查詢啟用的 AGV
curl "http://localhost:8000/api/v1/agv/?enabled_only=true"

# 分頁查詢
curl "http://localhost:8000/api/v1/agv/?skip=0&limit=10"
```

**回應**:
```json
[
  {
    "id": 1,
    "name": "AGV01",
    "description": "倉庫搬運車",
    "model": "K400",
    "enable": 1,
    "created_at": "2025-12-05T14:00:00",
    "updated_at": "2025-12-05T14:00:00"
  },
  {
    "id": 2,
    "name": "AGV02",
    "description": "大型貨運車",
    "model": "Cargo",
    "enable": 1,
    "created_at": "2025-12-05T14:01:00",
    "updated_at": "2025-12-05T14:01:00"
  }
]
```

---

### 3. 查詢單一 AGV

**端點**: `GET /api/v1/agv/{agv_id}`

**請求範例**:
```bash
curl "http://localhost:8000/api/v1/agv/1"
```

**回應**:
```json
{
  "id": 1,
  "name": "AGV01",
  "description": "倉庫搬運車",
  "model": "K400",
  "enable": 1,
  "created_at": "2025-12-05T14:00:00",
  "updated_at": "2025-12-05T14:00:00"
}
```

---

### 4. 更新 AGV（UPDATE - 完整更新）

**端點**: `PUT /api/v1/agv/{agv_id}`

**請求範例**:
```json
{
  "name": "AGV01",
  "model": "K400-Pro",
  "description": "倉庫搬運車（升級版）",
  "enable": 1
}
```

**cURL**:
```bash
curl -X PUT "http://localhost:8000/api/v1/agv/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AGV01",
    "model": "K400-Pro",
    "description": "倉庫搬運車（升級版）",
    "enable": 1
  }'
```

**回應**:
```json
{
  "id": 1,
  "name": "AGV01",
  "description": "倉庫搬運車（升級版）",
  "model": "K400-Pro",
  "enable": 1,
  "created_at": "2025-12-05T14:00:00",
  "updated_at": "2025-12-05T14:10:00"
}
```

---

### 5. 部分更新 AGV（UPDATE - 部分更新）

**端點**: `PATCH /api/v1/agv/{agv_id}`

**請求範例** (只更新 description):
```json
{
  "description": "新的描述"
}
```

**cURL**:
```bash
curl -X PATCH "http://localhost:8000/api/v1/agv/1" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "新的描述"
  }'
```

**回應**:
```json
{
  "id": 1,
  "name": "AGV01",
  "description": "新的描述",
  "model": "K400-Pro",
  "enable": 1,
  "created_at": "2025-12-05T14:00:00",
  "updated_at": "2025-12-05T14:15:00"
}
```

---

### 6. 刪除 AGV（DELETE）

**端點**: `DELETE /api/v1/agv/{agv_id}`

**請求範例**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/agv/1"
```

**回應**: `204 No Content` (成功刪除，無回應內容)

---

### 7. 計算 AGV 總數

**端點**: `GET /api/v1/agv/count/total`

**查詢參數**:
- `enabled_only` (bool): 只計算啟用的 AGV，預設 false

**請求範例**:
```bash
curl "http://localhost:8000/api/v1/agv/count/total"
curl "http://localhost:8000/api/v1/agv/count/total?enabled_only=true"
```

**回應**:
```json
{
  "total": 10,
  "enabled_only": false
}
```

---

## 錯誤回應

### 404 Not Found
```json
{
  "detail": "找不到 ID 為 99 的 AGV"
}
```

### 400 Bad Request
```json
{
  "detail": "AGV 名稱 'AGV01' 已存在"
}
```

---

## Python 範例

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/agv"

# 1. 新增 AGV
response = requests.post(f"{BASE_URL}/", json={
    "name": "AGV01",
    "model": "K400",
    "description": "倉庫搬運車",
    "enable": 1
})
print(response.json())

# 2. 查詢所有 AGV
response = requests.get(f"{BASE_URL}/")
print(response.json())

# 3. 查詢單一 AGV
response = requests.get(f"{BASE_URL}/1")
print(response.json())

# 4. 更新 AGV
response = requests.put(f"{BASE_URL}/1", json={
    "name": "AGV01",
    "model": "K400-Pro",
    "description": "升級版",
    "enable": 1
})
print(response.json())

# 5. 部分更新 AGV
response = requests.patch(f"{BASE_URL}/1", json={
    "description": "新描述"
})
print(response.json())

# 6. 刪除 AGV
response = requests.delete(f"{BASE_URL}/1")
print(response.status_code)  # 204
```

---

## 注意事項

1. **AGV 名稱唯一性**: `name` 欄位必須唯一，重複會回傳 400 錯誤
2. **必填欄位**: `name` 和 `model` 是必填欄位
3. **enable 欄位**: 1 = 啟用, 0 = 停用
4. **時間戳**: `created_at` 和 `updated_at` 由系統自動管理
5. **ID 欄位**: 新增時不需提供，由資料庫自動產生
