# 新增资料表完整指南

本指南将教你如何从零开始添加一个新的资料表，并创建完整的 CRUD API 功能。

## 目录

1. [概览](#概览)
2. [步骤 1: 创建数据模型](#步骤-1-创建数据模型)
3. [步骤 2: 创建 Pydantic Schemas](#步骤-2-创建-pydantic-schemas)
4. [步骤 3: 创建 CRUD 操作](#步骤-3-创建-crud-操作)
5. [步骤 4: 创建 API 路由](#步骤-4-创建-api-路由)
6. [步骤 5: 注册路由](#步骤-5-注册路由)
7. [步骤 6: 更新导入](#步骤-6-更新导入)
8. [步骤 7: 初始化数据库](#步骤-7-初始化数据库)
9. [完整示例](#完整示例)
10. [最佳实践](#最佳实践)

---

## 概览

### 文件结构

创建一个新表需要在以下位置添加文件：

```
db_api/
├── app/
│   ├── models/
│   │   ├── __init__.py          # 需要更新
│   │   └── your_table.py        # 新建 - 步骤 1
│   ├── schemas/
│   │   └── your_table.py        # 新建 - 步骤 2
│   ├── crud/
│   │   └── your_table.py        # 新建 - 步骤 3
│   ├── api/
│   │   └── v1/
│   │       └── your_table.py    # 新建 - 步骤 4
│   └── main.py                  # 需要更新 - 步骤 5
└── scripts/
    └── db_init.py               # 需要更新 - 步骤 6
```

### 命名规范

- **资料表名**: 小写，单数形式（例如：`station`，不是 `stations`）
- **Python 类名**: 大驼峰，单数形式（例如：`Station`）
- **文件名**: 小写，下划线分隔（例如：`station.py`）

---

## 步骤 1: 创建数据模型

### 位置
`app/models/your_table.py`

### 示例：创建 Station（站点）表

```python
"""
站点数据模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import ConfigDict


class Station(SQLModel, table=True):
    """站点表 - 记录 AGV 站点信息"""
    __tablename__ = "station"

    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)

    # 基本信息（必填字段）
    name: str = Field(
        unique=True,
        max_length=50,
        index=True,
        description="站点名称，唯一标识"
    )
    type: str = Field(
        max_length=20,
        description="站点类型：loading, unloading, charging, waiting"
    )

    # 可选字段（带默认值）
    description: str = Field(
        default="na",
        description="站点描述"
    )
    zone: str = Field(
        default="na",
        max_length=20,
        description="所属区域"
    )
    capacity: int = Field(
        default=1,
        description="容量（可停靠 AGV 数量）"
    )
    priority: int = Field(
        default=0,
        description="优先级"
    )

    # JSON 参数（带默认值）
    parameter: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {"x": 0, "y": 0, "z": 0},
        sa_column=Column(JSON),
        description="站点坐标参数（JSON 格式）"
    )

    # 时间戳（自动管理）
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="创建时间"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="更新时间"
    )

    model_config = ConfigDict(from_attributes=True)
```

### 字段类型说明

| Python 类型 | PostgreSQL 类型 | 说明 |
|------------|----------------|------|
| `int` | INTEGER | 整数 |
| `str` | VARCHAR | 字符串（需指定 max_length）|
| `float` | REAL | 浮点数 |
| `bool` | BOOLEAN | 布尔值 |
| `datetime` | TIMESTAMP | 时间戳 |
| `Dict[str, Any]` | JSON | JSON 对象 |
| `Optional[类型]` | 可为 NULL | 可选字段 |

### 字段属性

```python
Field(
    default=值,                    # 默认值
    default_factory=lambda: {},   # 默认值工厂（用于可变对象）
    primary_key=True,             # 主键
    unique=True,                  # 唯一约束
    index=True,                   # 创建索引
    max_length=50,                # 字符串最大长度
    description="说明"             # 字段说明（显示在 API 文档）
)
```

---

## 步骤 2: 创建 Pydantic Schemas

### 位置
`app/schemas/your_table.py`

### 示例

```python
"""
Station Schemas
用于 API 请求和响应的数据模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StationCreate(BaseModel):
    """新增 Station 的请求模型"""
    name: str = Field(..., description="站点名称（必填，唯一）")
    type: str = Field(..., description="站点类型（必填）")
    description: str = Field("na", description="站点描述，预设 na")
    zone: str = Field("na", description="所属区域，预设 na")
    capacity: int = Field(1, description="容量，预设 1")
    priority: int = Field(0, description="优先级，预设 0")
    parameter: Dict[str, Any] = Field(
        default_factory=lambda: {"x": 0, "y": 0, "z": 0},
        description="坐标参数，预设 {\"x\":0,\"y\":0,\"z\":0}"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "STATION_A",
                "type": "loading",
                "description": "na",
                "zone": "na",
                "capacity": 1,
                "priority": 0,
                "parameter": {"x": 0, "y": 0, "z": 0}
            }
        }
    )


class StationUpdate(BaseModel):
    """更新 Station 的请求模型 - 所有字段都是选填"""
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    zone: Optional[str] = None
    capacity: Optional[int] = None
    priority: Optional[int] = None
    parameter: Optional[Dict[str, Any]] = None


class StationResponse(BaseModel):
    """Station 响应模型"""
    id: int
    name: str
    type: str
    description: str
    zone: str
    capacity: int
    priority: int
    parameter: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### 说明

- **StationCreate**: 用于 POST 请求，只包含可提供的字段
- **StationUpdate**: 用于 PUT/PATCH 请求，所有字段都是可选
- **StationResponse**: 用于响应，包含所有字段（包括 id、时间戳）

---

## 步骤 3: 创建 CRUD 操作

### 位置
`app/crud/your_table.py`

### 示例

```python
"""
Station CRUD 操作

提供数据库层的增删改查操作
"""
from sqlmodel import Session, select
from app.models.station import Station
from datetime import datetime
from typing import Optional


def create_station(session: Session, station: Station) -> Station:
    """新增 Station"""
    session.add(station)
    session.commit()
    session.refresh(station)
    return station


def get_station(session: Session, station_id: int) -> Station | None:
    """根据 ID 查询单一 Station"""
    return session.get(Station, station_id)


def get_station_by_name(session: Session, name: str) -> Station | None:
    """根据名称查询 Station"""
    statement = select(Station).where(Station.name == name)
    return session.exec(statement).first()


def get_all_stations(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    zone: Optional[str] = None
) -> list[Station]:
    """
    查询所有 Station

    Args:
        session: 数据库 Session
        skip: 跳过笔数（分页用）
        limit: 限制笔数（分页用）
        type: 按类型筛选（选填）
        zone: 按区域筛选（选填）
    """
    statement = select(Station)

    # 筛选条件
    if type:
        statement = statement.where(Station.type == type)
    if zone:
        statement = statement.where(Station.zone == zone)

    # 排序和分页
    statement = statement.order_by(Station.priority.desc(), Station.name.asc())
    statement = statement.offset(skip).limit(limit)

    return list(session.exec(statement).all())


def update_station(session: Session, station_id: int, station_data: dict) -> Station | None:
    """更新 Station"""
    station = session.get(Station, station_id)
    if not station:
        return None

    # 更新字段
    for key, value in station_data.items():
        if hasattr(station, key) and key not in ['id', 'created_at']:
            setattr(station, key, value)

    # 更新时间戳
    station.updated_at = datetime.now()

    session.add(station)
    session.commit()
    session.refresh(station)
    return station


def delete_station(session: Session, station_id: int) -> bool:
    """删除 Station"""
    station = session.get(Station, station_id)
    if not station:
        return False

    session.delete(station)
    session.commit()
    return True


def count_stations(session: Session, type: Optional[str] = None) -> int:
    """计算 Station 总数"""
    statement = select(Station)

    if type:
        statement = statement.where(Station.type == type)

    return len(list(session.exec(statement).all()))
```

### 常用 CRUD 函数

| 函数名 | 用途 | 必须实现 |
|--------|------|---------|
| `create_xxx()` | 新增记录 | ✅ 是 |
| `get_xxx()` | 根据 ID 查询 | ✅ 是 |
| `get_xxx_by_name()` | 根据名称查询 | 推荐 |
| `get_all_xxx()` | 查询所有（支持筛选） | ✅ 是 |
| `update_xxx()` | 更新记录 | ✅ 是 |
| `delete_xxx()` | 删除记录 | ✅ 是 |
| `count_xxx()` | 统计数量 | 推荐 |

---

## 步骤 4: 创建 API 路由

### 位置
`app/api/v1/your_table.py`

### 示例

```python
"""
Station API 路由

提供站点相关的 RESTful API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

from app.core.database import get_session
from app.models.station import Station
from app.schemas.station import StationCreate, StationUpdate, StationResponse
from app.crud import station as crud_station

router = APIRouter()


@router.post("/", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def create_station(
    station_in: StationCreate,
    session: Session = Depends(get_session)
):
    """
    新增站点

    - **name**: 站点名称（必填，唯一）
    - **type**: 站点类型（必填）
    - 其他字段使用默认值
    """
    # 检查名称是否已存在
    existing = crud_station.get_station_by_name(session, station_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"站点名称 '{station_in.name}' 已存在"
        )

    # 转换为 Station 模型
    station_data = Station(**station_in.model_dump())
    station = crud_station.create_station(session, station_data)
    return station


@router.get("/", response_model=List[Station])
def get_all_stations(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = Query(None, description="按类型筛选"),
    zone: Optional[str] = Query(None, description="按区域筛选"),
    session: Session = Depends(get_session)
):
    """查询所有站点"""
    stations = crud_station.get_all_stations(
        session,
        skip=skip,
        limit=limit,
        type=type,
        zone=zone
    )
    return stations


@router.get("/{station_id}", response_model=Station)
def get_station(
    station_id: int,
    session: Session = Depends(get_session)
):
    """根据 ID 查询单一站点"""
    station = crud_station.get_station(session, station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 为 {station_id} 的站点"
        )
    return station


@router.put("/{station_id}", response_model=Station)
def update_station(
    station_id: int,
    station_in: Station,
    session: Session = Depends(get_session)
):
    """更新站点（完整更新）"""
    existing = crud_station.get_station(session, station_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 为 {station_id} 的站点"
        )

    # 检查名称冲突
    if station_in.name != existing.name:
        name_check = crud_station.get_station_by_name(session, station_in.name)
        if name_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"站点名称 '{station_in.name}' 已被使用"
            )

    update_data = station_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})
    station = crud_station.update_station(session, station_id, update_data)
    return station


@router.patch("/{station_id}", response_model=Station)
def partial_update_station(
    station_id: int,
    station_in: Station,
    session: Session = Depends(get_session)
):
    """部分更新站点"""
    existing = crud_station.get_station(session, station_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 为 {station_id} 的站点"
        )

    update_data = station_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    if 'name' in update_data and update_data['name'] != existing.name:
        name_check = crud_station.get_station_by_name(session, update_data['name'])
        if name_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"站点名称 '{update_data['name']}' 已被使用"
            )

    station = crud_station.update_station(session, station_id, update_data)
    return station


@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(
    station_id: int,
    session: Session = Depends(get_session)
):
    """删除站点"""
    success = crud_station.delete_station(session, station_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 为 {station_id} 的站点"
        )
    return None


@router.get("/count/total")
def count_stations(
    type: Optional[str] = Query(None, description="按类型筛选"),
    session: Session = Depends(get_session)
):
    """统计站点总数"""
    count = crud_station.count_stations(session, type=type)
    return {"total": count, "type": type}
```

### 标准 API 端点

| HTTP 方法 | 路径 | 功能 | 状态码 |
|----------|------|------|--------|
| POST | `/` | 新增 | 201 |
| GET | `/` | 查询所有（支持筛选） | 200 |
| GET | `/{id}` | 查询单个 | 200 |
| PUT | `/{id}` | 完整更新 | 200 |
| PATCH | `/{id}` | 部分更新 | 200 |
| DELETE | `/{id}` | 删除 | 204 |
| GET | `/count/total` | 统计数量 | 200 |

---

## 步骤 5: 注册路由

### 位置
`app/main.py`

### 修改内容

#### 5.1 导入路由

```python
from app.api.v1 import agv, eqp_port, task, station  # 添加 station
```

#### 5.2 注册路由

```python
# 注册 Station API 路由
app.include_router(
    station.router,
    prefix=f"{settings.API_V1_PREFIX}/station",
    tags=["Station"]
)
```

### 完整示例

```python
# 在 app/main.py 的路由注册部分添加

app.include_router(
    agv.router,
    prefix=f"{settings.API_V1_PREFIX}/agv",
    tags=["AGV"]
)

app.include_router(
    eqp_port.router,
    prefix=f"{settings.API_V1_PREFIX}/eqp_port",
    tags=["EqpPort"]
)

app.include_router(
    task.router,
    prefix=f"{settings.API_V1_PREFIX}/task",
    tags=["Task"]
)

# 新增
app.include_router(
    station.router,
    prefix=f"{settings.API_V1_PREFIX}/station",
    tags=["Station"]
)
```

---

## 步骤 6: 更新导入

### 6.1 更新 `app/models/__init__.py`

```python
"""
资料模型
"""
from .agv import AGV
from .eqp_port import EqpPort
from .task import Task
from .station import Station  # 新增

__all__ = ["AGV", "EqpPort", "Task", "Station"]  # 新增 Station
```

### 6.2 更新 `scripts/db_init.py`

```python
import psycopg2
from sqlmodel import SQLModel, create_engine
from app.models import AGV, EqpPort, Task, Station  # 新增 Station
```

---

## 步骤 7: 初始化数据库

### 7.1 删除旧表（如果已存在）

```bash
docker exec postgres psql -U agvc -d agvc -c "DROP TABLE IF EXISTS station CASCADE;"
```

### 7.2 运行初始化脚本

```bash
cd C:\Users\akifa\Documents\CASE\AGV專案\EBD_CT_派車系統\db_api
python scripts/db_init.py
```

### 7.3 验证表结构

```bash
docker exec postgres psql -U agvc -d agvc -c "\d station"
```

### 7.4 重启 API 服务器

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 7.5 测试 API

访问 http://localhost:8000/docs，查看新的 Station 端点

---

## 完整示例

以下是一个完整的"站点"（Station）表实现示例，包含所有必要的文件：

### 文件清单

```
✅ app/models/station.py          # 数据模型
✅ app/schemas/station.py         # Pydantic Schemas
✅ app/crud/station.py             # CRUD 操作
✅ app/api/v1/station.py           # API 路由
✅ app/models/__init__.py          # 已更新
✅ app/main.py                     # 已更新
✅ scripts/db_init.py              # 已更新
```

### 测试清单

- [ ] 创建站点（POST /api/v1/station/）
- [ ] 查询所有站点（GET /api/v1/station/）
- [ ] 查询单个站点（GET /api/v1/station/{id}）
- [ ] 更新站点（PUT /api/v1/station/{id}）
- [ ] 部分更新（PATCH /api/v1/station/{id}）
- [ ] 删除站点（DELETE /api/v1/station/{id}）
- [ ] 统计数量（GET /api/v1/station/count/total）

---

## 最佳实践

### 1. 命名规范

- **表名**: 小写单数（`station` 而非 `stations`）
- **类名**: 大驼峰单数（`Station`）
- **字段名**: 小写下划线（`created_at`）
- **路由前缀**: 小写单数（`/station`）

### 2. 字段设计

#### 必填字段
- 需要用户提供的关键信息
- 使用 `Field(...)` 标记为必填

#### 可选字段
- 有合理默认值的字段
- 使用 `Field(default=值)` 提供默认值

#### 字符串字段默认值
```python
# ✅ 推荐
description: str = Field(default="na", ...)

# ❌ 不推荐
description: Optional[str] = Field(default=None, ...)
```

#### 整数字段默认值
```python
# ✅ 推荐
priority: int = Field(default=0, ...)

# ❌ 不推荐
priority: Optional[int] = Field(default=None, ...)
```

### 3. 索引优化

为常用查询字段添加索引：

```python
name: str = Field(
    unique=True,  # 唯一约束自动创建索引
    index=True,   # 普通索引
    ...
)
```

### 4. 唯一约束

对于需要唯一性的字段（如名称、编号）：

```python
name: str = Field(unique=True, ...)
```

并在 API 中检查：

```python
existing = crud_xxx.get_xxx_by_name(session, xxx_in.name)
if existing:
    raise HTTPException(
        status_code=400,
        detail=f"名称 '{xxx_in.name}' 已存在"
    )
```

### 5. 时间戳管理

```python
# 创建时间 - 插入时自动设置
created_at: Optional[datetime] = Field(
    default_factory=datetime.now,
    ...
)

# 更新时间 - 插入时自动设置，更新时手动设置
updated_at: Optional[datetime] = Field(
    default_factory=datetime.now,
    ...
)
```

在 CRUD 的 update 函数中：

```python
def update_xxx(session: Session, xxx_id: int, xxx_data: dict):
    # ...
    xxx.updated_at = datetime.now()  # 手动更新时间戳
    # ...
```

### 6. JSON 字段

```python
parameter: Optional[Dict[str, Any]] = Field(
    default_factory=lambda: {"key": "value"},  # 使用 lambda
    sa_column=Column(JSON),                    # 指定 SQL 类型
    ...
)
```

### 7. API 文档优化

为每个字段添加清晰的描述：

```python
name: str = Field(
    ...,
    description="站点名称（必填，唯一）"  # 在 Swagger UI 中显示
)
```

添加示例：

```python
model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "name": "STATION_A",
            "type": "loading",
            ...
        }
    }
)
```

### 8. 错误处理

```python
# 404 - 资源不存在
if not xxx:
    raise HTTPException(
        status_code=404,
        detail=f"找不到 ID 为 {xxx_id} 的资源"
    )

# 400 - 业务逻辑错误（如重复名称）
if existing:
    raise HTTPException(
        status_code=400,
        detail=f"名称 '{name}' 已存在"
    )
```

### 9. 查询优化

支持常用筛选：

```python
def get_all_xxx(
    session: Session,
    skip: int = 0,        # 分页
    limit: int = 100,     # 分页
    type: str = None,     # 筛选
    zone: str = None      # 筛选
):
    statement = select(XXX)

    if type:
        statement = statement.where(XXX.type == type)
    if zone:
        statement = statement.where(XXX.zone == zone)

    # 排序
    statement = statement.order_by(XXX.priority.desc())

    # 分页
    statement = statement.offset(skip).limit(limit)

    return list(session.exec(statement).all())
```

### 10. 测试检查清单

创建新表后，务必测试：

- [ ] 数据库表是否创建成功
- [ ] 字段类型是否正确
- [ ] 索引是否创建
- [ ] 默认值是否生效
- [ ] API 端点是否可访问
- [ ] 创建操作是否正常
- [ ] 查询操作是否正常
- [ ] 更新操作是否正常
- [ ] 删除操作是否正常
- [ ] Swagger UI 是否正确显示

---

## 常见问题

### Q1: 修改表结构后如何更新数据库？

```bash
# 删除旧表
docker exec postgres psql -U agvc -d agvc -c "DROP TABLE IF EXISTS your_table CASCADE;"

# 重新创建
python scripts/db_init.py
```

### Q2: 如何添加外键关联？

```python
from sqlmodel import Field, Relationship

class Task(SQLModel, table=True):
    agv_id: int = Field(foreign_key="agv.id")
    agv: Optional["AGV"] = Relationship(back_populates="tasks")
```

### Q3: 如何添加复合索引？

```python
from sqlalchemy import Index

class MyTable(SQLModel, table=True):
    __tablename__ = "my_table"

    field1: str
    field2: str

    __table_args__ = (
        Index('idx_field1_field2', 'field1', 'field2'),
    )
```

### Q4: 如何处理软删除？

添加 `is_deleted` 字段：

```python
is_deleted: bool = Field(default=False, description="软删除标记")
```

在查询时过滤：

```python
statement = select(XXX).where(XXX.is_deleted == False)
```

---

## 快速参考

### 创建新表的完整流程

```bash
# 1. 创建文件
app/models/your_table.py
app/schemas/your_table.py
app/crud/your_table.py
app/api/v1/your_table.py

# 2. 更新文件
app/models/__init__.py
app/main.py
scripts/db_init.py

# 3. 初始化数据库
python scripts/db_init.py

# 4. 重启服务器
# Ctrl+C 停止
python -m uvicorn app.main:app --reload --port 8000

# 5. 测试
# 访问 http://localhost:8000/docs
```

---

## 总结

按照本指南的 7 个步骤，你可以快速添加新的资料表并创建完整的 CRUD API。记住：

1. ✅ 遵循命名规范
2. ✅ 为字段设置合理的默认值
3. ✅ 添加必要的索引和约束
4. ✅ 提供清晰的 API 文档
5. ✅ 进行完整的功能测试

祝你开发顺利！
