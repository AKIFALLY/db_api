"""
AGV CRUD 操作

提供資料庫層的增刪改查操作
"""
from sqlmodel import Session, select
from app.models import AGV
from datetime import datetime


def create_agv(session: Session, agv: AGV) -> AGV:
    """
    新增 AGV

    Args:
        session: 資料庫 Session
        agv: AGV 物件

    Returns:
        新建的 AGV 物件
    """
    session.add(agv)
    session.commit()
    session.refresh(agv)
    return agv


def get_agv(session: Session, agv_id: int) -> AGV | None:
    """
    根據 ID 查詢單一 AGV

    Args:
        session: 資料庫 Session
        agv_id: AGV ID

    Returns:
        AGV 物件或 None
    """
    return session.get(AGV, agv_id)


def get_agv_by_name(session: Session, name: str) -> AGV | None:
    """
    根據名稱查詢 AGV

    Args:
        session: 資料庫 Session
        name: AGV 名稱

    Returns:
        AGV 物件或 None
    """
    statement = select(AGV).where(AGV.name == name)
    return session.exec(statement).first()


def get_all_agvs(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    enabled_only: bool = False
) -> list[AGV]:
    """
    查詢所有 AGV

    Args:
        session: 資料庫 Session
        skip: 跳過筆數（分頁用）
        limit: 限制筆數（分頁用）
        enabled_only: 是否只查詢啟用的 AGV

    Returns:
        AGV 物件列表
    """
    statement = select(AGV)

    if enabled_only:
        statement = statement.where(AGV.enable == 1)

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_agv(session: Session, agv_id: int, agv_data: dict) -> AGV | None:
    """
    更新 AGV

    Args:
        session: 資料庫 Session
        agv_id: AGV ID
        agv_data: 要更新的資料（字典）

    Returns:
        更新後的 AGV 物件或 None
    """
    agv = session.get(AGV, agv_id)
    if not agv:
        return None

    # 更新欄位
    for key, value in agv_data.items():
        if hasattr(agv, key) and key not in ['id', 'created_at']:  # 不允許更新 id 和 created_at
            setattr(agv, key, value)

    # 更新時間戳
    agv.updated_at = datetime.now()

    session.add(agv)
    session.commit()
    session.refresh(agv)
    return agv


def delete_agv(session: Session, agv_id: int) -> bool:
    """
    刪除 AGV

    Args:
        session: 資料庫 Session
        agv_id: AGV ID

    Returns:
        是否成功刪除
    """
    agv = session.get(AGV, agv_id)
    if not agv:
        return False

    session.delete(agv)
    session.commit()
    return True


def count_agvs(session: Session, enabled_only: bool = False) -> int:
    """
    計算 AGV 總數

    Args:
        session: 資料庫 Session
        enabled_only: 是否只計算啟用的 AGV

    Returns:
        AGV 總數
    """
    statement = select(AGV)

    if enabled_only:
        statement = statement.where(AGV.enable == 1)

    return len(list(session.exec(statement).all()))
