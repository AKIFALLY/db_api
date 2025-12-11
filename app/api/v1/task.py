"""
Task API 路由

提供任務相關的 RESTful API 端點
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

from app.core.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud import task as crud_task

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    新增任務

    - **work_id**: 工作 ID（必填）
    - **from_port**: 起始端口（必填）
    - **to_port**: 目標端口（必填）
    - **status_id**: 任務狀態 ID（必填）
    - **parent_task_id**: 父任務 ID（選填）
    - **agv_name**: 執行任務的 AGV 名稱（選填）
    - **priority**: 優先級，預設 0
    - **material_code**: 物料代碼（選填）
    - **parameters**: 任務參數（JSON，選填）
    """
    # 轉換為 Task 模型
    task_data = Task(**task_in.model_dump())
    task = crud_task.create_task(session, task_data)
    return task


@router.get("/", response_model=List[Task])
def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    status_id: Optional[int] = Query(None, description="按狀態 ID 篩選"),
    agv_name: Optional[str] = Query(None, description="按 AGV 名稱篩選"),
    work_id: Optional[int] = Query(None, description="按工作 ID 篩選"),
    session: Session = Depends(get_session)
):
    """
    查詢所有任務

    - **skip**: 跳過筆數（分頁用），預設 0
    - **limit**: 限制筆數（分頁用），預設 100
    - **status_id**: 按狀態 ID 篩選（選填）
    - **agv_name**: 按 AGV 名稱篩選（選填）
    - **work_id**: 按工作 ID 篩選（選填）

    結果按優先級（降序）和創建時間（升序）排序
    """
    tasks = crud_task.get_all_tasks(
        session,
        skip=skip,
        limit=limit,
        status_id=status_id,
        agv_name=agv_name,
        work_id=work_id
    )
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """
    根據 ID 查詢單一任務

    - **task_id**: 任務 ID
    """
    task = crud_task.get_task(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {task_id} 的任務"
        )
    return task


@router.get("/{parent_task_id}/children", response_model=List[Task])
def get_child_tasks(
    parent_task_id: int,
    session: Session = Depends(get_session)
):
    """
    查詢子任務

    - **parent_task_id**: 父任務 ID
    """
    # 先檢查父任務是否存在
    parent_task = crud_task.get_task(session, parent_task_id)
    if not parent_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {parent_task_id} 的父任務"
        )

    tasks = crud_task.get_tasks_by_parent(session, parent_task_id)
    return tasks


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_in: Task,
    session: Session = Depends(get_session)
):
    """
    更新任務（完整更新）

    - **task_id**: 任務 ID
    - **task_in**: 更新的任務資料
    """
    # 檢查任務是否存在
    existing_task = crud_task.get_task(session, task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {task_id} 的任務"
        )

    # 轉換為字典（排除 None 值）
    update_data = task_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    task = crud_task.update_task(session, task_id, update_data)
    return task


@router.patch("/{task_id}", response_model=Task)
def partial_update_task(
    task_id: int,
    task_in: Task,
    session: Session = Depends(get_session)
):
    """
    部分更新任務（只更新提供的欄位）

    - **task_id**: 任務 ID
    - **task_in**: 要更新的欄位
    """
    # 檢查任務是否存在
    existing_task = crud_task.get_task(session, task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {task_id} 的任務"
        )

    # 轉換為字典（只包含有設定的欄位）
    update_data = task_in.model_dump(exclude_unset=True, exclude={'id', 'created_at'})

    task = crud_task.update_task(session, task_id, update_data)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """
    刪除任務

    - **task_id**: 任務 ID
    """
    success = crud_task.delete_task(session, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {task_id} 的任務"
        )
    return None


@router.get("/count/total")
def count_tasks(
    status_id: Optional[int] = Query(None, description="按狀態 ID 篩選"),
    agv_name: Optional[str] = Query(None, description="按 AGV 名稱篩選"),
    session: Session = Depends(get_session)
):
    """
    計算任務總數

    - **status_id**: 按狀態 ID 篩選（選填）
    - **agv_name**: 按 AGV 名稱篩選（選填）
    """
    count = crud_task.count_tasks(session, status_id=status_id, agv_name=agv_name)
    return {"total": count, "status_id": status_id, "agv_name": agv_name}
