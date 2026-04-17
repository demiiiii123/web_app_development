import sqlite3
import os

def get_db_connection():
    """
    取得 SQLite 資料庫連線。
    預設取得 instance/database.db，並設定 row_factory 以便用欄位名稱存取。
    """
    try:
        # 指向專案根目錄底下的 instance/database.db
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, 'instance', 'database.db')
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"資料庫連線錯誤: {e}")
        return None
