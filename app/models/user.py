import sqlite3
from . import get_db_connection

def create(data):
    """
    新增一名會員記錄。
    :param data: 字典，包含 'username' 與 'password_hash'
    :return: 新增的會員 ID (成功)，或 None (失敗)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users (username, password_hash)
               VALUES (?, ?)""",
            (data.get('username'), data.get('password_hash'))
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except sqlite3.Error as e:
        print(f"User create 錯誤: {e}")
        return None

def get_all():
    """
    取得所有會員記錄。
    :return: 會員紀錄列表列表
    """
    try:
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM users").fetchall()
        conn.close()
        return [dict(row) for row in users]
    except sqlite3.Error as e:
        print(f"User get_all 錯誤: {e}")
        return []

def get_by_id(user_id):
    """
    依照 ID 取得單筆會員紀錄。
    :param user_id: 會員 ID
    :return: 包含會員資料的字典，若無則回傳 None
    """
    try:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"User get_by_id 錯誤: {e}")
        return None

def get_by_username(username):
    """
    依照使用者名稱取得單筆會員紀錄 (常登入驗證使用)。
    :param username: 使用者名稱
    :return: 包含會員資料的字典，若無則回傳 None
    """
    try:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"User get_by_username 錯誤: {e}")
        return None

def update(user_id, data):
    """
    更新特定會員記錄 (例如更新密碼或勝率積分)。
    :param user_id: 會員 ID
    :param data: 包含欲更新欄位與值的字典
    :return: 布林值表示是否成功
    """
    try:
        conn = get_db_connection()
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        values = list(data.values())
        values.append(user_id)
        
        sql = f"UPDATE users SET {set_clause} WHERE id = ?"
        conn.execute(sql, values)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"User update 錯誤: {e}")
        return False

def delete(user_id):
    """
    刪除指定會員記錄。
    :param user_id: 會員 ID
    :return: 布林值表示是否成功
    """
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"User delete 錯誤: {e}")
        return False
