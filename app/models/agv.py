"""
AGVC 系統資料模型定義

使用 SQLModel (基於 SQLAlchemy 和 Pydantic)
"""
from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import ConfigDict


class AGV(SQLModel, table=True):
    """AGV 車輛主表 - 只包含靜態屬性"""
    __tablename__ = "agv"

    # 主鍵
    id: Optional[int] = Field(default=None, primary_key=True)

    # 基本資訊
    name: str = Field(
        unique=True,
        max_length=20,
        index=True,
        description="AGV 名稱/編號，如 AGV01"
    )
    description: Optional[str] = Field(
        default=None,
        description="AGV 描述"
    )
    model: str = Field(
        max_length=50,
        description="AGV 型號：K400, Cargo, Loader, Unloader"
    )

    # 啟用狀態
    enable: int = Field(default=1, description="啟用狀態：1=啟用, 0=停用")

    # 參數設定（JSON 欄位）
    parameter: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="AGV 參數設定（JSON 格式）"
    )

    # 時間戳記
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="建立時間"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="更新時間"
    )

    model_config = ConfigDict(from_attributes=True)
