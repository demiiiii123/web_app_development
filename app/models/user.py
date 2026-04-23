from .db import get_db_connection

class User:
    def __init__(self, id, username, is_guest, created_at):
        self.id = id
        self.username = username
        self.is_guest = is_guest
        self.created_at = created_at

    @staticmethod
    def create(username, is_guest=True):
        """新增一筆玩家記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, is_guest) VALUES (?, ?)',
                (username, is_guest)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return User.get_by_id(user_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得單筆玩家記錄"""
        try:
            conn = get_db_connection()
            user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            
            if user_row:
                return User(
                    id=user_row['id'],
                    username=user_row['username'],
                    is_guest=user_row['is_guest'],
                    created_at=user_row['created_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有玩家記錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return [
                User(
                    id=row['id'],
                    username=row['username'],
                    is_guest=row['is_guest'],
                    created_at=row['created_at']
                ) for row in rows
            ]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def update(user_id, username):
        """更新玩家記錄"""
        try:
            conn = get_db_connection()
            conn.execute('UPDATE users SET username = ? WHERE id = ?', (username, user_id))
            conn.commit()
            conn.close()
            return User.get_by_id(user_id)
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    @staticmethod
    def delete(user_id):
        """刪除玩家記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
