from .db import get_db_connection

class GameHistory:
    def __init__(self, id, room_id, winner_id, ended_at):
        self.id = id
        self.room_id = room_id
        self.winner_id = winner_id
        self.ended_at = ended_at

    @staticmethod
    def create(room_id, winner_id):
        """建立遊戲歷史紀錄"""
        try:
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
        except Exception as e:
            print(f"Error creating game history: {e}")
            return None

    @staticmethod
    def get_by_id(history_id):
        """根據 ID 取得遊戲歷史紀錄"""
        try:
            conn = get_db_connection()
            row = conn.execute('SELECT * FROM game_histories WHERE id = ?', (history_id,)).fetchone()
            conn.close()
            if row:
                return GameHistory(row['id'], row['room_id'], row['winner_id'], row['ended_at'])
            return None
        except Exception as e:
            print(f"Error getting game history by id: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有遊戲歷史紀錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute('SELECT * FROM game_histories').fetchall()
            conn.close()
            return [GameHistory(row['id'], row['room_id'], row['winner_id'], row['ended_at']) for row in rows]
        except Exception as e:
            print(f"Error getting all game histories: {e}")
            return []

    @staticmethod
    def update(history_id, winner_id):
        """更新遊戲歷史紀錄（實務上較少用到）"""
        try:
            conn = get_db_connection()
            conn.execute('UPDATE game_histories SET winner_id = ? WHERE id = ?', (winner_id, history_id))
            conn.commit()
            conn.close()
            return GameHistory.get_by_id(history_id)
        except Exception as e:
            print(f"Error updating game history: {e}")
            return None

    @staticmethod
    def delete(history_id):
        """刪除遊戲歷史紀錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM game_histories WHERE id = ?', (history_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting game history: {e}")
            return False

    @staticmethod
    def get_user_histories(user_id):
        """取得某位玩家參與過的所有遊戲紀錄"""
        try:
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
        except Exception as e:
            print(f"Error getting user histories: {e}")
            return []
