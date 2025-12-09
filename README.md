# AGVC 系統 API

AGV 車輛管理系統 FastAPI 後端服務

## 專案結構

```
db_api/
├── app/                          # 主應用程式
│   ├── __init__.py
│   ├── main.py                  # FastAPI 應用入口（待建立）
│   ├── models/                  # 資料模型（SQLModel）
│   │   ├── __init__.py
│   │   └── agv.py              # AGV 模型
│   ├── crud/                    # CRUD 操作
│   │   ├── __init__.py
│   │   └── agv.py              # AGV CRUD（待建立）
│   ├── api/                     # API 路由
│   │   ├── __init__.py
│   │   └── v1/                 # API v1
│   │       ├── __init__.py
│   │       └── agv.py          # AGV 路由（待建立）
│   └── core/                    # 核心配置
│       ├── __init__.py
│       ├── config.py           # 系統配置
│       └── database.py         # 資料庫連線管理
├── scripts/                     # 工具腳本
│   └── db_init.py              # 資料庫初始化工具
├── examples/                    # 範例程式
│   └── crud_example.py         # CRUD 操作示範
├── docs/                        # 文檔
│   └── DATABASE_CONNECTION.md  # 資料庫連線說明
├── docker-compose.yaml          # Docker 配置
├── requirements.txt             # Python 依賴
└── README.md                    # 本文件
```

## 安裝

### 1. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 2. 啟動 PostgreSQL

```bash
docker-compose up -d postgres
```

### 3. 初始化資料庫

```bash
python scripts/db_init.py
```

## 資料庫配置

- **主機**: localhost
- **端口**: 5432
- **用戶**: agvc
- **密碼**: 36274806
- **資料庫**: agvc

詳細說明請參考 [docs/DATABASE_CONNECTION.md](docs/DATABASE_CONNECTION.md)

## 開發

### 執行 CRUD 範例

```bash
python examples/crud_example.py
```

### 啟動 API 服務（待實作）

```bash
uvicorn app.main:app --reload
```

API 文檔: http://localhost:8000/docs

## 技術棧

- **FastAPI** - Web 框架
- **SQLModel** - ORM（結合 SQLAlchemy + Pydantic）
- **PostgreSQL** - 資料庫
- **Docker** - 容器化

## 資料模型

### AGV（車輛）

- `id` - 主鍵（自增）
- `name` - AGV 名稱/編號（唯一）
- `description` - 描述
- `model` - 型號
- `enable` - 啟用狀態
- `created_at` - 建立時間
- `updated_at` - 更新時間

## 下一步

- [ ] 建立 FastAPI 主程式 (`app/main.py`)
- [ ] 建立 AGV CRUD 操作 (`app/crud/agv.py`)
- [ ] 建立 AGV API 路由 (`app/api/v1/agv.py`)
- [ ] 加入其他資料模型（站點、任務等）
- [ ] 實作 WebSocket 即時通訊
- [ ] 加入認證與授權
