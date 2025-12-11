"""
日志配置
- 自动轮转（每天一个文件或达到大小限制）
- 保留最近 30 天的日志
- 限制单个文件最大 10MB
"""
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path


def setup_logging():
    """配置日志系统"""

    # 创建 logs 目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. 访问日志（按大小轮转）
    access_handler = RotatingFileHandler(
        log_dir / "access.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=30,  # 保留 30 个备份文件
        encoding='utf-8'
    )
    access_handler.setFormatter(log_format)
    access_handler.setLevel(logging.INFO)

    # 2. 错误日志（按天轮转）
    error_handler = TimedRotatingFileHandler(
        log_dir / "error.log",
        when='midnight',  # 每天午夜轮转
        interval=1,
        backupCount=30,  # 保留 30 天
        encoding='utf-8'
    )
    error_handler.setFormatter(log_format)
    error_handler.setLevel(logging.ERROR)

    # 3. 应用日志（按大小轮转）
    app_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,  # 保留 10 个备份
        encoding='utf-8'
    )
    app_handler.setFormatter(log_format)
    app_handler.setLevel(logging.INFO)

    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(access_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(app_handler)

    # 配置 uvicorn 日志
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.addHandler(access_handler)

    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.addHandler(error_handler)

    # 配置应用日志
    app_logger = logging.getLogger("app")
    app_logger.addHandler(app_handler)

    return root_logger


# 获取应用日志器
def get_logger(name: str = "app"):
    """获取日志器"""
    return logging.getLogger(name)
