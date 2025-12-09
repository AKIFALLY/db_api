"""
EqpPort API 路由

提供設備端口相關的 RESTful API 端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.models.eqp_port import EqpPort
from app.schemas.eqp_port import EqpPortCreate, EqpPortUpdate, EqpPortResponse
from app.crud import eqp_port as crud_eqp_port

router = APIRouter()


@router.post("/", response_model=EqpPortResponse, status_code=status.HTTP_201_CREATED)
def create_eqp_port(
    eqp_port_in: EqpPortCreate,
    session: Session = Depends(get_session)
):
    """
    新增設備端口

    - **name**: 端口名稱（必填，唯一）
    - **eqp_name**: 所屬設備名稱（必填）
    - **node**: 節點編號（必填）
    - **description**: 描述（選填）
    - **parameter**: 端口參數（JSON，選填）
    """
    # 檢查名稱是否已存在
    existing_port = crud_eqp_port.get_eqp_port_by_name(session, eqp_port_in.name)
    if existing_port:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"端口名稱 '{eqp_port_in.name}' 已存在"
        )

    # 轉換為 EqpPort 模型
    eqp_port_data = EqpPort(**eqp_port_in.model_dump())
    eqp_port = crud_eqp_port.create_eqp_port(session, eqp_port_data)
    return eqp_port


@router.get("/", response_model=List[EqpPort])
def get_all_eqp_ports(
    skip: int = 0,
    limit: int = 100,
    eqp_name: str | None = None,
    session: Session = Depends(get_session)
):
    """
    查詢所有設備端口

    - **skip**: 跳過筆數（分頁用），預設 0
    - **limit**: 限制筆數（分頁用），預設 100
    - **eqp_name**: 按設備名稱篩選（選填）
    """
    eqp_ports = crud_eqp_port.get_all_eqp_ports(
        session,
        skip=skip,
        limit=limit,
        eqp_name=eqp_name
    )
    return eqp_ports


@router.get("/{eqp_port_id}", response_model=EqpPort)
def get_eqp_port(
    eqp_port_id: int,
    session: Session = Depends(get_session)
):
    """
    根據 ID 查詢單一設備端口

    - **eqp_port_id**: 端口 ID
    """
    eqp_port = crud_eqp_port.get_eqp_port(session, eqp_port_id)
    if not eqp_port:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {eqp_port_id} 的設備端口"
        )
    return eqp_port


@router.put("/{eqp_port_id}", response_model=EqpPort)
def update_eqp_port(
    eqp_port_id: int,
    eqp_port_in: EqpPort,
    session: Session = Depends(get_session)
):
    """
    更新設備端口（完整更新）

    - **eqp_port_id**: 端口 ID
    - **eqp_port_in**: 更新的端口資料
    """
    # 檢查端口是否存在
    existing_port = crud_eqp_port.get_eqp_port(session, eqp_port_id)
    if not existing_port:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {eqp_port_id} 的設備端口"
        )

    # 如果要更新名稱，檢查新名稱是否已被其他端口使用
    if eqp_port_in.name != existing_port.name:
        name_check = crud_eqp_port.get_eqp_port_by_name(session, eqp_port_in.name)
        if name_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"端口名稱 '{eqp_port_in.name}' 已被其他端口使用"
            )

    # 轉換為字典（排除 None 值）
    update_data = eqp_port_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    eqp_port = crud_eqp_port.update_eqp_port(session, eqp_port_id, update_data)
    return eqp_port


@router.patch("/{eqp_port_id}", response_model=EqpPort)
def partial_update_eqp_port(
    eqp_port_id: int,
    eqp_port_in: EqpPort,
    session: Session = Depends(get_session)
):
    """
    部分更新設備端口（只更新提供的欄位）

    - **eqp_port_id**: 端口 ID
    - **eqp_port_in**: 要更新的欄位
    """
    # 檢查端口是否存在
    existing_port = crud_eqp_port.get_eqp_port(session, eqp_port_id)
    if not existing_port:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {eqp_port_id} 的設備端口"
        )

    # 轉換為字典（只包含有設定的欄位）
    update_data = eqp_port_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    # 如果要更新名稱，檢查新名稱是否已被其他端口使用
    if 'name' in update_data and update_data['name'] != existing_port.name:
        name_check = crud_eqp_port.get_eqp_port_by_name(session, update_data['name'])
        if name_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"端口名稱 '{update_data['name']}' 已被其他端口使用"
            )

    eqp_port = crud_eqp_port.update_eqp_port(session, eqp_port_id, update_data)
    return eqp_port


@router.delete("/{eqp_port_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_eqp_port(
    eqp_port_id: int,
    session: Session = Depends(get_session)
):
    """
    刪除設備端口

    - **eqp_port_id**: 端口 ID
    """
    success = crud_eqp_port.delete_eqp_port(session, eqp_port_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {eqp_port_id} 的設備端口"
        )
    return None


@router.get("/count/total")
def count_eqp_ports(
    eqp_name: str | None = None,
    session: Session = Depends(get_session)
):
    """
    計算設備端口總數

    - **eqp_name**: 按設備名稱篩選（選填）
    """
    count = crud_eqp_port.count_eqp_ports(session, eqp_name=eqp_name)
    return {"total": count, "eqp_name": eqp_name}
