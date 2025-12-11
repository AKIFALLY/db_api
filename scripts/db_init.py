"""
資料庫初始化工具

功能：
1. 測試資料庫連線
2. 使用 SQLModel 建立資料表
3. 列出所有資料庫
"""
import sys
from pathlib import Path

# 加入專案根目錄到 Python 路徑
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import psycopg2
from sqlmodel import SQLModel, create_engine
from app.models import AGV, EqpPort, Task

# 從 docker-compose.yaml 讀取的資料庫連線資訊
DB_CONFIG = {
    'host': 'localhost',  # 從 host 機器連接使用 localhost（容器內部 IP: 192.168.100.254）
    'port': 5432,
    'user': 'agvc',
    'password': '36274806',
    'database': 'agvc'  # 連接到 docker-compose 建立的預設資料庫
}

# SQLAlchemy 連線字串
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


def test_connection():
    """
    測試資料庫連線並列出所有資料庫
    """
    conn = None
    try:
        print("正在連接到 PostgreSQL 伺服器...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("[成功] 連線成功！")

        cursor = conn.cursor()

        # 獲取 PostgreSQL 版本
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\nPostgreSQL 版本: {version.split(',')[0]}")

        # 列出所有資料庫
        cursor.execute("""
            SELECT datname, pg_size_pretty(pg_database_size(datname)) as size
            FROM pg_database
            WHERE datistemplate = false
            ORDER BY datname;
        """)
        databases = cursor.fetchall()

        print("\n現有資料庫:")
        print("-" * 40)
        for db_name, size in databases:
            print(f"  - {db_name:<15} ({size})")
        print("-" * 40)

        cursor.close()
        return True

    except psycopg2.Error as e:
        print(f"[失敗] 資料庫錯誤: {e}")
        return False
    except Exception as e:
        print(f"[失敗] 發生錯誤: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("\n資料庫連線已關閉")


def create_tables():
    """
    使用 SQLModel 建立所有資料表
    """
    try:
        print("\n" + "=" * 50)
        print("開始建立資料表...")
        print("=" * 50)

        # 建立 engine
        engine = create_engine(DATABASE_URL, echo=True)  # echo=True 會顯示 SQL 語句

        # 建立所有表
        SQLModel.metadata.create_all(engine)

        print("\n" + "=" * 50)
        print("[成功] 資料表建立完成！")
        print("=" * 50)

        # 列出已建立的表
        print("\n已建立的資料表:")
        print("-" * 40)
        for table_name in SQLModel.metadata.tables.keys():
            print(f"  - {table_name}")
        print("-" * 40)

        return True

    except Exception as e:
        print(f"\n[失敗] 建立資料表時發生錯誤: {e}")
        return False


def main():
    """主函數"""
    print("=" * 50)
    print("PostgreSQL 資料庫管理工具")
    print("=" * 50)
    print(f"主機: {DB_CONFIG['host']}")
    print(f"端口: {DB_CONFIG['port']}")
    print(f"用戶: {DB_CONFIG['user']}")
    print(f"資料庫: {DB_CONFIG['database']}")
    print("=" * 50)
    print()

    # 1. 測試連線
    if not test_connection():
        print("\n資料庫連線失敗，請檢查設定")
        return

    # 2. 建立資料表
    create_tables()

    print("\n" + "=" * 50)
    print("操作完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()
