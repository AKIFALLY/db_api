"""
Task Schemas
用於 API 請求和回應的資料模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """新增 Task 的請求模型"""
    parent_task_id: int = Field(0, description="父任務 ID，預設 0 表示無父任務")
    work_id: int = Field(..., description="工作 ID（必填）")
    from_port: str = Field("na", description="起始端口，預設 na")
    to_port: str = Field("na", description="目標端口，預設 na")
    status_id: int = Field(..., description="任務狀態 ID（必填）")
    agv_name: str = Field("na", description="執行任務的 AGV 名稱，預設 na")
    priority: int = Field(0, description="優先級（數字越大優先級越高），預設 0")
    material_code: str = Field("na", description="物料代碼，預設 na")
    parameter: Dict[str, Any] = Field(
        default_factory=lambda: {"pr1": "na"},
        description="任務參數設定（JSON 格式），預設為 {\"pr1\":\"na\"}"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "work_id": 1,
                "status_id": 1,
                "parent_task_id": 0,
                "from_port": "na",
                "to_port": "na",
                "agv_name": "na",
                "priority": 0,
                "material_code": "na",
                "parameter": {"pr1": "na"}
            }
        }
    )


class TaskUpdate(BaseModel):
    """更新 Task 的請求模型 - 所有欄位都是選填"""
    parent_task_id: Optional[int] = None
    work_id: Optional[int] = None
    from_port: Optional[str] = None
    to_port: Optional[str] = None
    status_id: Optional[int] = None
    agv_name: Optional[str] = None
    priority: Optional[int] = None
    material_code: Optional[str] = None
    parameter: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    """Task 回應模型 - 固定欄位順序"""
    id: int
    parent_task_id: int
    work_id: int
    from_port: str
    to_port: str
    status_id: int
    agv_name: str
    priority: int
    material_code: str
    parameter: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
