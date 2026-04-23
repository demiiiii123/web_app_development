from .db import get_db_connection

class GameHistory:
    def __init__(self, id, room_id, winner_id, ended_at):
        self.id = id
        self.room_id = room_id
        self.winner_id = winner_id
        self.ended_at = ended_at

    @staticmethod
    def create(room_id, winner_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO game_histories (room_id, winner_id) VALUES (?, ?)',
            (room_id, winner_id)
        )
        conn.commit()
        history_id = cursor.lastrowid
        conn.close()
        return GameHistory.get_by_id(history_id)

    @staticmethod
    def get_by_id(history_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM game_histories WHERE id = ?', (history_id,)).fetchone()
        conn.close()
        if row:
            return GameHistory(row['id'], row['room_id'], row['winner_id'], row['ended_at'])
        return None

    @staticmethod
    def get_user_histories(user_id):
        """取得某位玩家參與過的所有遊戲紀錄"""
        conn = get_db_connection()
        rows = conn.execute('''
            SELECT gh.*, r.invite_code 
            FROM game_histories gh
            JOIN rooms r ON gh.room_id = r.id
            JOIN room_players rp ON r.id = rp.room_id
            WHERE rp.user_id = ?
            ORDER BY gh.ended_at DESC
        ''', (user_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]
