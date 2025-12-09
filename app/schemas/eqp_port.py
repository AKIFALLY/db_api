"""
EqpPort Schemas
用於 API 請求和回應的資料模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class EqpPortCreate(BaseModel):
    """新增 EqpPort 的請求模型 - 只包含可提供的欄位"""
    name: str = Field(..., description="端口名稱，唯一識別")
    eqp_name: str = Field(..., description="所屬設備名稱")
    node: str = Field(..., description="節點編號")
    description: Optional[str] = Field("N/A", description="端口描述，預設為 N/A")
    parameter: Optional[Dict[str, Any]] = Field(None, description="端口參數設定（JSON 格式）")


class EqpPortUpdate(BaseModel):
    """更新 EqpPort 的請求模型 - 所有欄位都是選填"""
    name: Optional[str] = None
    eqp_name: Optional[str] = None
    node: Optional[str] = None
    description: Optional[str] = None
    parameter: Optional[Dict[str, Any]] = None


class EqpPortResponse(BaseModel):
    """EqpPort 回應模型 - 固定欄位順序"""
    id: int
    name: str
    eqp_name: str
    node: str
    description: Optional[str] = None
    parameter: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
