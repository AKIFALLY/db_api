"""
AGV Schemas
用於 API 請求和回應的資料模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class AGVCreate(BaseModel):
    """新增 AGV 的請求模型 - 只包含可提供的欄位"""
    name: str = Field(..., description="AGV 名稱/編號，如 AGV01（必填）")
    model: str = Field(..., description="AGV 型號：K400, Cargo, Loader, Unloader（必填）")
    description: Optional[str] = Field("N/A", description="AGV 描述，預設為 N/A")
    enable: int = Field(1, description="啟用狀態：1=啟用, 0=停用")
    parameter: Dict[str, Any] = Field(
        default_factory=lambda: {"ip": "", "port": 0, "work_id": 0},
        description="AGV 參數設定（JSON 格式），預設為 {\"ip\":\"\",\"port\":0,\"work_id\":0}"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "AGV01",
                "model": "K400",
                "description": "N/A",
                "enable": 1,
                "parameter": {"ip": "", "port": 0, "work_id": 0}
            }
        }
    )


class AGVUpdate(BaseModel):
    """更新 AGV 的請求模型 - 所有欄位都是選填"""
    name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    enable: Optional[int] = None
    parameter: Optional[Dict[str, Any]] = None


class AGVResponse(BaseModel):
    """AGV 回應模型 - 固定欄位順序"""
    id: int
    name: str
    description: Optional[str] = None
    model: str
    enable: int
    parameter: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
