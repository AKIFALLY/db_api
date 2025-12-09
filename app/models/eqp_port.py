"""
AGVC 系統資料模型 - 設備端口
"""
from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import ConfigDict


class EqpPort(SQLModel, table=True):
    """設備端口表 - 記錄設備的端口資訊"""
    __tablename__ = "eqp_port"

    # 主鍵
    id: Optional[int] = Field(default=None, primary_key=True)

    # 基本資訊
    name: str = Field(
        unique=True,
        max_length=50,
        index=True,
        description="端口名稱，唯一識別"
    )
    eqp_name: str = Field(
        max_length=50,
        index=True,
        description="所屬設備名稱"
    )
    node: str = Field(
        max_length=50,
        description="節點編號"
    )
    description: Optional[str] = Field(
        default=None,
        description="端口描述"
    )

    # 參數設定（JSON 欄位）
    parameter: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="端口參數設定（JSON 格式）"
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
