import sqlite3
from . import get_db_connection

def create(data):
    """
    新增一筆遊戲房間記錄。
    :param data: 字典，包含 'name', 'host_id', 以及選填的 'password'
    :return: 新建房間的 ID (成功)，或 None (失敗)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO rooms (name, password, host_id, status)
               VALUES (?, ?, ?, 'waiting')""",
            (data.get('name'), data.get('password', ''), data.get('host_id'))
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except sqlite3.Error as e:
        print(f"Room create 錯誤: {e}")
        return None

def get_all():
    """
    取得所有房間記錄，包含狀態為 waiting 的房間 (可作為大廳使用)。
    :return: 房間紀錄列表
    """
    try:
        conn = get_db_connection()
        # 加入 JOIN 以取得房主名稱
        sql = """SELECT rooms.*, users.username AS host_name 
                 FROM rooms 
                 LEFT JOIN users ON rooms.host_id = users.id
                 ORDER BY rooms.created_at DESC"""
        rooms = conn.execute(sql).fetchall()
        conn.close()
        return [dict(row) for row in rooms]
    except sqlite3.Error as e:
        print(f"Room get_all 錯誤: {e}")
        return []

def get_by_id(room_id):
    """
    依照 ID 取得單筆房間紀錄。
    :param room_id: 房間 ID
    :return: 包含房間資訊的字典，若無則為 None
    """
    try:
        conn = get_db_connection()
        room = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
        conn.close()
        return dict(room) if room else None
    except sqlite3.Error as e:
        print(f"Room get_by_id 錯誤: {e}")
        return None

def update(room_id, data):
    """
    更新特定房間記錄 (例如遊戲狀態改變：waiting -> playing -> closed)。
    :param room_id: 房間 ID
    :param data: 欲更新的欄位字典
    :return: 是否成功更新
    """
    try:
        conn = get_db_connection()
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        values = list(data.values())
        values.append(room_id)
        
        sql = f"UPDATE rooms SET {set_clause} WHERE id = ?"
        conn.execute(sql, values)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Room update 錯誤: {e}")
        return False

def delete(room_id):
    """
    刪除特定房間 (例如遊戲結束解散)。
    :param room_id: 房間 ID
    :return: 是否成功刪除
    """
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Room delete 錯誤: {e}")
        return False
