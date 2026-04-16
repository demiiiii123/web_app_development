from . import get_db

class GameHistory:
    @staticmethod
    def create(room_id, winner_id, game_type, start_time):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO game_history (room_id, winner_id, game_type, start_time) VALUES (?, ?, ?, ?)",
            (room_id, winner_id, game_type, start_time)
        )
        conn.commit()
        history_id = cursor.lastrowid
        conn.close()
        return history_id

    @staticmethod
    def get_by_id(history_id):
        conn = get_db()
        history = conn.execute("SELECT * FROM game_history WHERE id = ?", (history_id,)).fetchone()
        conn.close()
        return dict(history) if history else None

    @staticmethod
    def get_by_user(user_id):
        conn = get_db()
        query = """
            SELECT gh.*, r.name as room_name
            FROM game_history gh
            LEFT JOIN rooms r ON gh.room_id = r.id
            JOIN room_players rp ON rp.room_id = gh.room_id
            WHERE rp.user_id = ?
            ORDER BY gh.end_time DESC
        """
        histories = conn.execute(query, (user_id,)).fetchall()
        conn.close()
        return [dict(h) for h in histories]

    @staticmethod
    def update_end_time(history_id, end_time):
        conn = get_db()
        conn.execute("UPDATE game_history SET end_time = ? WHERE id = ?", (end_time, history_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(history_id):
        conn = get_db()
        conn.execute("DELETE FROM game_history WHERE id = ?", (history_id,))
        conn.commit()
        conn.close()
