"""
Task CRUD 操作

提供資料庫層的增刪改查操作
"""
from sqlmodel import Session, select
from app.models.task import Task
from datetime import datetime
from typing import Optional


def create_task(session: Session, task: Task) -> Task:
    """
    新增 Task

    Args:
        session: 資料庫 Session
        task: Task 物件

    Returns:
        新建的 Task 物件
    """
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int) -> Task | None:
    """
    根據 ID 查詢單一 Task

    Args:
        session: 資料庫 Session
        task_id: Task ID

    Returns:
        Task 物件或 None
    """
    return session.get(Task, task_id)


def get_all_tasks(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    status_id: Optional[int] = None,
    agv_name: Optional[str] = None,
    work_id: Optional[int] = None
) -> list[Task]:
    """
    查詢所有 Task

    Args:
        session: 資料庫 Session
        skip: 跳過筆數（分頁用）
        limit: 限制筆數（分頁用）
        status_id: 按狀態 ID 篩選（選填）
        agv_name: 按 AGV 名稱篩選（選填）
        work_id: 按工作 ID 篩選（選填）

    Returns:
        Task 物件列表
    """
    statement = select(Task)

    # 篩選條件
    if status_id is not None:
        statement = statement.where(Task.status_id == status_id)
    if agv_name:
        statement = statement.where(Task.agv_name == agv_name)
    if work_id is not None:
        statement = statement.where(Task.work_id == work_id)

    # 按優先級和創建時間排序
    statement = statement.order_by(Task.priority.desc(), Task.created_at.asc())
    statement = statement.offset(skip).limit(limit)

    return list(session.exec(statement).all())


def get_tasks_by_parent(session: Session, parent_task_id: int) -> list[Task]:
    """
    查詢子任務

    Args:
        session: 資料庫 Session
        parent_task_id: 父任務 ID

    Returns:
        子任務列表
    """
    statement = select(Task).where(Task.parent_task_id == parent_task_id)
    return list(session.exec(statement).all())


def update_task(session: Session, task_id: int, task_data: dict) -> Task | None:
    """
    更新 Task

    Args:
        session: 資料庫 Session
        task_id: Task ID
        task_data: 要更新的資料（字典）

    Returns:
        更新後的 Task 物件或 None
    """
    task = session.get(Task, task_id)
    if not task:
        return None

    # 更新欄位
    for key, value in task_data.items():
        if hasattr(task, key) and key not in ['id', 'created_at']:  # 不允許更新 id 和 created_at
            setattr(task, key, value)

    # 更新時間戳
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    """
    刪除 Task

    Args:
        session: 資料庫 Session
        task_id: Task ID

    Returns:
        是否成功刪除
    """
    task = session.get(Task, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def count_tasks(
    session: Session,
    status_id: Optional[int] = None,
    agv_name: Optional[str] = None
) -> int:
    """
    計算 Task 總數

    Args:
        session: 資料庫 Session
        status_id: 按狀態 ID 篩選（選填）
        agv_name: 按 AGV 名稱篩選（選填）

    Returns:
        Task 總數
    """
    statement = select(Task)

    if status_id is not None:
        statement = statement.where(Task.status_id == status_id)
    if agv_name:
        statement = statement.where(Task.agv_name == agv_name)

    return len(list(session.exec(statement).all()))
