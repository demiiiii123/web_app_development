from .db import get_db_connection
import string
import random

class Room:
    def __init__(self, id, invite_code, host_id, status, created_at):
        self.id = id
        self.invite_code = invite_code
        self.host_id = host_id
        self.status = status
        self.created_at = created_at

    @staticmethod
    def _generate_invite_code(length=6):
        letters_and_digits = string.ascii_uppercase + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    @staticmethod
    def create(host_id):
        """建立一個新房間"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 產生唯一邀請碼
            while True:
                invite_code = Room._generate_invite_code()
                exist = cursor.execute('SELECT id FROM rooms WHERE invite_code = ?', (invite_code,)).fetchone()
                if not exist:
                    break

            cursor.execute(
                'INSERT INTO rooms (invite_code, host_id, status) VALUES (?, ?, ?)',
                (invite_code, host_id, 'waiting')
            )
            conn.commit()
            room_id = cursor.lastrowid
            conn.close()
            return Room.get_by_id(room_id)
        except Exception as e:
            print(f"Error creating room: {e}")
            return None

    @staticmethod
    def get_by_id(room_id):
        """根據 ID 取得房間記錄"""
        try:
            conn = get_db_connection()
            row = conn.execute('SELECT * FROM rooms WHERE id = ?', (room_id,)).fetchone()
            conn.close()
            if row:
                return Room(row['id'], row['invite_code'], row['host_id'], row['status'], row['created_at'])
            return None
        except Exception as e:
            print(f"Error getting room by id: {e}")
            return None

    @staticmethod
    def get_by_invite_code(invite_code):
        """根據邀請碼取得房間記錄"""
        try:
            conn = get_db_connection()
            row = conn.execute('SELECT * FROM rooms WHERE invite_code = ?', (invite_code,)).fetchone()
            conn.close()
            if row:
                return Room(row['id'], row['invite_code'], row['host_id'], row['status'], row['created_at'])
            return None
        except Exception as e:
            print(f"Error getting room by invite code: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有房間記錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute('SELECT * FROM rooms').fetchall()
            conn.close()
            return [Room(row['id'], row['invite_code'], row['host_id'], row['status'], row['created_at']) for row in rows]
        except Exception as e:
            print(f"Error getting all rooms: {e}")
            return []

    @staticmethod
    def update_status(room_id, status):
        """更新房間狀態"""
        try:
            conn = get_db_connection()
            conn.execute('UPDATE rooms SET status = ? WHERE id = ?', (status, room_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating room status: {e}")
            return False

    @staticmethod
    def delete(room_id):
        """刪除房間記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting room: {e}")
            return False


class RoomPlayer:
    @staticmethod
    def join_room(room_id, user_id):
        """玩家加入房間"""
        try:
            conn = get_db_connection()
            # 檢查是否已在房間內
            exist = conn.execute('SELECT id FROM room_players WHERE room_id = ? AND user_id = ?', (room_id, user_id)).fetchone()
            if not exist:
                conn.execute(
                    'INSERT INTO room_players (room_id, user_id, score, is_ready) VALUES (?, ?, 0, 0)',
                    (room_id, user_id)
                )
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error joining room: {e}")
            return False

    @staticmethod
    def get_players_in_room(room_id):
        """取得房間內所有玩家狀態"""
        try:
            conn = get_db_connection()
            rows = conn.execute('''
                SELECT rp.*, u.username, u.is_guest 
                FROM room_players rp
                JOIN users u ON rp.user_id = u.id
                WHERE rp.room_id = ?
            ''', (room_id,)).fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting players in room: {e}")
            return []

    @staticmethod
    def update_score(room_id, user_id, score_delta):
        """更新玩家在房間內的分數"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE room_players SET score = score + ? WHERE room_id = ? AND user_id = ?',
                (score_delta, room_id, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating player score: {e}")
            return False
    
    @staticmethod
    def leave_room(room_id, user_id):
        """玩家離開房間"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM room_players WHERE room_id = ? AND user_id = ?', (room_id, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error leaving room: {e}")
            return False
