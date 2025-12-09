"""
EqpPort CRUD 操作

提供資料庫層的增刪改查操作
"""
from sqlmodel import Session, select
from app.models.eqp_port import EqpPort
from datetime import datetime


def create_eqp_port(session: Session, eqp_port: EqpPort) -> EqpPort:
    """
    新增 EqpPort

    Args:
        session: 資料庫 Session
        eqp_port: EqpPort 物件

    Returns:
        新建的 EqpPort 物件
    """
    session.add(eqp_port)
    session.commit()
    session.refresh(eqp_port)
    return eqp_port


def get_eqp_port(session: Session, eqp_port_id: int) -> EqpPort | None:
    """
    根據 ID 查詢單一 EqpPort

    Args:
        session: 資料庫 Session
        eqp_port_id: EqpPort ID

    Returns:
        EqpPort 物件或 None
    """
    return session.get(EqpPort, eqp_port_id)


def get_eqp_port_by_name(session: Session, name: str) -> EqpPort | None:
    """
    根據名稱查詢 EqpPort

    Args:
        session: 資料庫 Session
        name: 端口名稱

    Returns:
        EqpPort 物件或 None
    """
    statement = select(EqpPort).where(EqpPort.name == name)
    return session.exec(statement).first()


def get_all_eqp_ports(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    eqp_name: str | None = None
) -> list[EqpPort]:
    """
    查詢所有 EqpPort

    Args:
        session: 資料庫 Session
        skip: 跳過筆數（分頁用）
        limit: 限制筆數（分頁用）
        eqp_name: 按設備名稱篩選（選填）

    Returns:
        EqpPort 物件列表
    """
    statement = select(EqpPort)

    if eqp_name:
        statement = statement.where(EqpPort.eqp_name == eqp_name)

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_eqp_port(session: Session, eqp_port_id: int, eqp_port_data: dict) -> EqpPort | None:
    """
    更新 EqpPort

    Args:
        session: 資料庫 Session
        eqp_port_id: EqpPort ID
        eqp_port_data: 要更新的資料（字典）

    Returns:
        更新後的 EqpPort 物件或 None
    """
    eqp_port = session.get(EqpPort, eqp_port_id)
    if not eqp_port:
        return None

    # 更新欄位
    for key, value in eqp_port_data.items():
        if hasattr(eqp_port, key) and key not in ['id', 'created_at']:  # 不允許更新 id 和 created_at
            setattr(eqp_port, key, value)

    # 更新時間戳
    eqp_port.updated_at = datetime.now()

    session.add(eqp_port)
    session.commit()
    session.refresh(eqp_port)
    return eqp_port


def delete_eqp_port(session: Session, eqp_port_id: int) -> bool:
    """
    刪除 EqpPort

    Args:
        session: 資料庫 Session
        eqp_port_id: EqpPort ID

    Returns:
        是否成功刪除
    """
    eqp_port = session.get(EqpPort, eqp_port_id)
    if not eqp_port:
        return False

    session.delete(eqp_port)
    session.commit()
    return True


def count_eqp_ports(session: Session, eqp_name: str | None = None) -> int:
    """
    計算 EqpPort 總數

    Args:
        session: 資料庫 Session
        eqp_name: 按設備名稱篩選（選填）

    Returns:
        EqpPort 總數
    """
    statement = select(EqpPort)

    if eqp_name:
        statement = statement.where(EqpPort.eqp_name == eqp_name)

    return len(list(session.exec(statement).all()))
