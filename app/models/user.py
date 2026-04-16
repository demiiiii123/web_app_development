from . import get_db

class User:
    @staticmethod
    def create(username, password_hash):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db()
        users = conn.execute("SELECT * FROM users ORDER BY points DESC").fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update_stats(user_id, won=False, points_earned=0):
        conn = get_db()
        if won:
            conn.execute(
                "UPDATE users SET matches_played = matches_played + 1, matches_won = matches_won + 1, points = points + ? WHERE id = ?",
                (points_earned, user_id)
            )
        else:
            conn.execute(
                "UPDATE users SET matches_played = matches_played + 1, points = points + ? WHERE id = ?",
                (points_earned, user_id)
            )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
