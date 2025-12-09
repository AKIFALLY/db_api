"""
AGV CRUD 操作範例

示範如何使用 SQLModel 對 AGV 表進行增刪改查操作
"""
import sys
from pathlib import Path

# 加入專案根目錄到 Python 路徑
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from sqlmodel import Session, create_engine, select
from app.models import AGV

# 資料庫連線
DATABASE_URL = "postgresql://agvc:36274806@localhost:5432/agvc"
engine = create_engine(DATABASE_URL)


# ==================== Create (新增) ====================

def create_agv(name: str, model: str, description: str = None) -> AGV:
    """
    新增一台 AGV

    Args:
        name: AGV 名稱/編號，如 'AGV01'
        model: AGV 型號，如 'K400'
        description: 描述（選填）

    Returns:
        新建的 AGV 物件
    """
    with Session(engine) as session:
        agv = AGV(
            name=name,
            model=model,
            description=description,
            enable=1  # 預設啟用
        )
        session.add(agv)
        session.commit()
        session.refresh(agv)  # 重新載入以獲取資料庫產生的 ID 和時間戳
        print(f"[新增] 成功新增 AGV: {agv.name} (ID: {agv.id})")
        return agv


# ==================== Read (讀取) ====================

def get_agv_by_id(agv_id: int) -> AGV | None:
    """
    根據 ID 查詢 AGV

    Args:
        agv_id: AGV ID

    Returns:
        AGV 物件或 None
    """
    with Session(engine) as session:
        agv = session.get(AGV, agv_id)
        if agv:
            print(f"[查詢] 找到 AGV: {agv.name} (ID: {agv.id})")
        else:
            print(f"[查詢] 找不到 ID 為 {agv_id} 的 AGV")
        return agv


def get_agv_by_name(name: str) -> AGV | None:
    """
    根據名稱查詢 AGV

    Args:
        name: AGV 名稱

    Returns:
        AGV 物件或 None
    """
    with Session(engine) as session:
        statement = select(AGV).where(AGV.name == name)
        agv = session.exec(statement).first()
        if agv:
            print(f"[查詢] 找到 AGV: {agv.name} (ID: {agv.id})")
        else:
            print(f"[查詢] 找不到名稱為 {name} 的 AGV")
        return agv


def get_all_agvs() -> list[AGV]:
    """
    查詢所有 AGV

    Returns:
        AGV 物件列表
    """
    with Session(engine) as session:
        statement = select(AGV)
        agvs = session.exec(statement).all()
        print(f"[查詢] 共找到 {len(agvs)} 台 AGV")
        return list(agvs)


def get_agvs_by_model(model: str) -> list[AGV]:
    """
    根據型號查詢 AGV

    Args:
        model: AGV 型號

    Returns:
        AGV 物件列表
    """
    with Session(engine) as session:
        statement = select(AGV).where(AGV.model == model)
        agvs = session.exec(statement).all()
        print(f"[查詢] 找到 {len(agvs)} 台型號為 {model} 的 AGV")
        return list(agvs)


def get_enabled_agvs() -> list[AGV]:
    """
    查詢所有啟用的 AGV

    Returns:
        啟用的 AGV 物件列表
    """
    with Session(engine) as session:
        statement = select(AGV).where(AGV.enable == 1)
        agvs = session.exec(statement).all()
        print(f"[查詢] 找到 {len(agvs)} 台已啟用的 AGV")
        return list(agvs)


# ==================== Update (更新) ====================

def update_agv(agv_id: int, **kwargs) -> AGV | None:
    """
    更新 AGV 資訊

    Args:
        agv_id: AGV ID
        **kwargs: 要更新的欄位（name, model, description, enable）

    Returns:
        更新後的 AGV 物件或 None
    """
    with Session(engine) as session:
        agv = session.get(AGV, agv_id)
        if not agv:
            print(f"[更新] 找不到 ID 為 {agv_id} 的 AGV")
            return None

        # 更新欄位
        for key, value in kwargs.items():
            if hasattr(agv, key):
                setattr(agv, key, value)

        from datetime import datetime
        agv.updated_at = datetime.now()  # 更新時間戳

        session.add(agv)
        session.commit()
        session.refresh(agv)
        print(f"[更新] 成功更新 AGV: {agv.name} (ID: {agv.id})")
        return agv


def enable_agv(agv_id: int) -> AGV | None:
    """
    啟用 AGV

    Args:
        agv_id: AGV ID

    Returns:
        更新後的 AGV 物件或 None
    """
    return update_agv(agv_id, enable=1)


def disable_agv(agv_id: int) -> AGV | None:
    """
    停用 AGV

    Args:
        agv_id: AGV ID

    Returns:
        更新後的 AGV 物件或 None
    """
    return update_agv(agv_id, enable=0)


# ==================== Delete (刪除) ====================

def delete_agv(agv_id: int) -> bool:
    """
    刪除 AGV

    Args:
        agv_id: AGV ID

    Returns:
        是否成功刪除
    """
    with Session(engine) as session:
        agv = session.get(AGV, agv_id)
        if not agv:
            print(f"[刪除] 找不到 ID 為 {agv_id} 的 AGV")
            return False

        session.delete(agv)
        session.commit()
        print(f"[刪除] 成功刪除 AGV: {agv.name} (ID: {agv_id})")
        return True


# ==================== 示範程式 ====================

def demo():
    """示範 CRUD 操作"""

    print("=" * 60)
    print("AGV CRUD 操作示範")
    print("=" * 60)

    # 1. 新增 AGV
    print("\n【1. 新增 AGV】")
    agv1 = create_agv(name="AGV01", model="K400", description="倉庫搬運車")
    agv2 = create_agv(name="AGV02", model="Cargo", description="大型貨運車")
    agv3 = create_agv(name="AGV03", model="K400")

    # 2. 查詢 AGV
    print("\n【2. 查詢 AGV】")
    get_agv_by_id(1)
    get_agv_by_name("AGV01")

    print("\n所有 AGV:")
    agvs = get_all_agvs()
    for agv in agvs:
        print(f"  - {agv.name} ({agv.model}) - 狀態: {'啟用' if agv.enable else '停用'}")

    print("\n型號為 K400 的 AGV:")
    k400_agvs = get_agvs_by_model("K400")
    for agv in k400_agvs:
        print(f"  - {agv.name}")

    # 3. 更新 AGV
    print("\n【3. 更新 AGV】")
    update_agv(1, description="倉庫搬運車（更新）", model="K400-Pro")

    # 4. 停用/啟用 AGV
    print("\n【4. 停用/啟用 AGV】")
    disable_agv(2)

    print("\n已啟用的 AGV:")
    enabled_agvs = get_enabled_agvs()
    for agv in enabled_agvs:
        print(f"  - {agv.name}")

    enable_agv(2)

    # 5. 刪除 AGV
    print("\n【5. 刪除 AGV】")
    delete_agv(3)

    print("\n最終所有 AGV:")
    agvs = get_all_agvs()
    for agv in agvs:
        print(f"  - ID:{agv.id} {agv.name} ({agv.model}) - {agv.description or '無描述'}")

    print("\n" + "=" * 60)
    print("示範完成！")
    print("=" * 60)


if __name__ == "__main__":
    demo()
