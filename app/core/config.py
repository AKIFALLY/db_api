"""
系統配置
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """系統設定"""

    # 資料庫設定
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "agvc"
    DB_PASSWORD: str = "36274806"
    DB_NAME: str = "agvc"

    # API 設定
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AGVC System"
    VERSION: str = "0.1.0"

    # CORS 設定
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    @property
    def DATABASE_URL(self) -> str:
        """資料庫連線字串"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        case_sensitive = True


# 全域設定實例
settings = Settings()
