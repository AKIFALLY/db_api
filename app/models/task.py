"""
AGVC 系統資料模型 - 任務表
"""
from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import ConfigDict


class Task(SQLModel, table=True):
    """任務表 - 記錄 AGV 執行的任務資訊"""
    __tablename__ = "task"

    # 主鍵
    id: Optional[int] = Field(default=None, primary_key=True)

    # 任務關聯
    parent_task_id: int = Field(
        default=0,
        index=True,
        description="父任務 ID，用於子任務關聯，0 表示無父任務"
    )
    work_id: int = Field(
        index=True,
        description="工作 ID"
    )

    # 端口資訊
    from_port: str = Field(
        default="na",
        max_length=50,
        description="起始端口"
    )
    to_port: str = Field(
        default="na",
        max_length=50,
        description="目標端口"
    )

    # 狀態和執行資訊
    status_id: int = Field(
        index=True,
        description="任務狀態 ID"
    )
    agv_name: str = Field(
        default="na",
        max_length=20,
        index=True,
        description="執行任務的 AGV 名稱"
    )

    # 任務屬性
    priority: int = Field(
        default=0,
        description="優先級（數字越大優先級越高）"
    )
    material_code: str = Field(
        default="na",
        max_length=50,
        description="物料代碼"
    )

    # 參數設定（JSON 欄位）
    parameter: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {"pr1": "na"},
        sa_column=Column(JSON),
        description="任務參數設定（JSON 格式）"
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
