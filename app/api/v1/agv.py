"""
AGV API 路由

提供 AGV 相關的 RESTful API 端點
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import time
from datetime import datetime

from app.core.database import get_session
from app.models import AGV
from app.schemas.agv import AGVCreate, AGVUpdate, AGVResponse
from app.crud import agv as crud_agv

router = APIRouter()


@router.post("/", response_model=AGVResponse, status_code=status.HTTP_201_CREATED)
def create_agv(
    agv_in: AGVCreate,
    session: Session = Depends(get_session)
):
    """
    新增 AGV

    - **name**: AGV 名稱/編號（必填，唯一）
    - **model**: AGV 型號（必填）
    - **description**: 描述（選填）
    - **enable**: 啟用狀態，預設 1
    - **parameter**: AGV 參數（JSON，選填）
    """
    # 檢查名稱是否已存在
    existing_agv = crud_agv.get_agv_by_name(session, agv_in.name)
    if existing_agv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AGV 名稱 '{agv_in.name}' 已存在"
        )

    # 轉換為 AGV 模型
    agv_data = AGV(**agv_in.model_dump())
    agv = crud_agv.create_agv(session, agv_data)
    return agv


@router.get("/", response_model=List[AGV])
def get_all_agvs(
    skip: int = 0,
    limit: int = 100,
    enabled_only: bool = False,
    session: Session = Depends(get_session)
):
    """
    查詢所有 AGV

    - **skip**: 跳過筆數（分頁用），預設 0
    - **limit**: 限制筆數（分頁用），預設 100
    - **enabled_only**: 是否只查詢啟用的 AGV，預設 False
    """
    agvs = crud_agv.get_all_agvs(
        session,
        skip=skip,
        limit=limit,
        enabled_only=enabled_only
    )
    return agvs


@router.get("/{agv_id}", response_model=AGV)
def get_agv(
    agv_id: int,
    session: Session = Depends(get_session)
):
    """
    根據 ID 查詢單一 AGV

    - **agv_id**: AGV ID
    """
    agv = crud_agv.get_agv(session, agv_id)
    if not agv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {agv_id} 的 AGV"
        )
    return agv


@router.put("/{agv_id}", response_model=AGV)
def update_agv(
    agv_id: int,
    agv_in: AGV,
    session: Session = Depends(get_session)
):
    """
    更新 AGV（完整更新）

    - **agv_id**: AGV ID
    - **agv_in**: 更新的 AGV 資料
    """
    # 檢查 AGV 是否存在
    existing_agv = crud_agv.get_agv(session, agv_id)
    if not existing_agv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {agv_id} 的 AGV"
        )

    # 如果要更新名稱，檢查新名稱是否已被其他 AGV 使用
    if agv_in.name != existing_agv.name:
        name_check = crud_agv.get_agv_by_name(session, agv_in.name)
        if name_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"AGV 名稱 '{agv_in.name}' 已被其他 AGV 使用"
            )

    # 轉換為字典（排除 None 值）
    update_data = agv_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    agv = crud_agv.update_agv(session, agv_id, update_data)
    return agv


@router.patch("/{agv_id}", response_model=AGV)
def partial_update_agv(
    agv_id: int,
    agv_in: AGV,
    session: Session = Depends(get_session)
):
    """
    部分更新 AGV（只更新提供的欄位）

    - **agv_id**: AGV ID
    - **agv_in**: 要更新的欄位
    """
    # 檢查 AGV 是否存在
    existing_agv = crud_agv.get_agv(session, agv_id)
    if not existing_agv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {agv_id} 的 AGV"
        )

    # 轉換為字典（只包含有設定的欄位）
    update_data = agv_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    # 如果要更新名稱，檢查新名稱是否已被其他 AGV 使用
    if 'name' in update_data and update_data['name'] != existing_agv.name:
        name_check = crud_agv.get_agv_by_name(session, update_data['name'])
        if name_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"AGV 名稱 '{update_data['name']}' 已被其他 AGV 使用"
            )

    agv = crud_agv.update_agv(session, agv_id, update_data)
    return agv


@router.delete("/{agv_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agv(
    agv_id: int,
    session: Session = Depends(get_session)
):
    """
    刪除 AGV

    - **agv_id**: AGV ID
    """
    success = crud_agv.delete_agv(session, agv_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {agv_id} 的 AGV"
        )
    return None


@router.get("/count/total")
def count_agvs(
    enabled_only: bool = False,
    session: Session = Depends(get_session)
):
    """
    計算 AGV 總數

    - **enabled_only**: 是否只計算啟用的 AGV，預設 False
    """
    count = crud_agv.count_agvs(session, enabled_only=enabled_only)
    return {"total": count, "enabled_only": enabled_only}


@router.get("/test/slow-query")
def test_slow_query(seconds: int = 10):
    """
    測試慢查詢 - 模擬資料庫查詢耗時

    用途：驗證在慢查詢執行期間，其他 API 請求是否仍能被處理

    測試方法：
    1. 開啟瀏覽器 A，訪問 /api/v1/agv/test/slow-query?seconds=10
    2. 立即開啟瀏覽器 B，訪問 /api/v1/agv/ （快速查詢）
    3. 如果瀏覽器 B 立即返回結果，證明可以併發處理

    - **seconds**: 模擬查詢耗時（秒），預設 10 秒
    """
    start_time = datetime.now()
    print(f"[慢查詢開始] {start_time.strftime('%H:%M:%S')} - 將耗時 {seconds} 秒")

    # 模擬慢查詢（例如複雜的 JOIN 或大量資料處理）
    time.sleep(seconds)

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    print(f"[慢查詢結束] {end_time.strftime('%H:%M:%S')} - 實際耗時 {elapsed:.2f} 秒")

    return {
        "message": "慢查詢測試完成",
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
        "elapsed_seconds": elapsed,
        "note": "如果在此查詢執行期間，其他 API 仍能回應，代表 FastAPI 線程池正常工作"
    }
