from .db import get_db_connection

class User:
    def __init__(self, id, username, is_guest, created_at):
        self.id = id
        self.username = username
        self.is_guest = is_guest
        self.created_at = created_at

    @staticmethod
    def create(username, is_guest=True):
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

    @staticmethod
    def get_by_id(user_id):
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

    @staticmethod
    def update(user_id, username):
        conn = get_db_connection()
        conn.execute('UPDATE users SET username = ? WHERE id = ?', (username, user_id))
        conn.commit()
        conn.close()
        return User.get_by_id(user_id)

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
