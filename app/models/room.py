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

    @staticmethod
    def get_by_id(room_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM rooms WHERE id = ?', (room_id,)).fetchone()
        conn.close()
        if row:
            return Room(row['id'], row['invite_code'], row['host_id'], row['status'], row['created_at'])
        return None

    @staticmethod
    def get_by_invite_code(invite_code):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM rooms WHERE invite_code = ?', (invite_code,)).fetchone()
        conn.close()
        if row:
            return Room(row['id'], row['invite_code'], row['host_id'], row['status'], row['created_at'])
        return None

    @staticmethod
    def update_status(room_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE rooms SET status = ? WHERE id = ?', (status, room_id))
        conn.commit()
        conn.close()


class RoomPlayer:
    @staticmethod
    def join_room(room_id, user_id):
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

    @staticmethod
    def get_players_in_room(room_id):
        conn = get_db_connection()
        rows = conn.execute('''
            SELECT rp.*, u.username, u.is_guest 
            FROM room_players rp
            JOIN users u ON rp.user_id = u.id
            WHERE rp.room_id = ?
        ''', (room_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update_score(room_id, user_id, score_delta):
        conn = get_db_connection()
        conn.execute(
            'UPDATE room_players SET score = score + ? WHERE room_id = ? AND user_id = ?',
            (score_delta, room_id, user_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def leave_room(room_id, user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM room_players WHERE room_id = ? AND user_id = ?', (room_id, user_id))
        conn.commit()
        conn.close()
