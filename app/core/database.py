"""
資料庫連線管理
"""
from sqlmodel import create_engine, Session
from .config import settings

# 建立資料庫引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # 生產環境設為 False
    pool_pre_ping=True,  # 檢查連線是否有效
)


def get_session():
    """
    取得資料庫 Session（用於 FastAPI 依賴注入）

    Yields:
        Session: 資料庫 Session
    """
    with Session(engine) as session:
        yield session
