from . import get_db

class Room:
    @staticmethod
    def create(name, password, max_players, host_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rooms (name, password, max_players, host_id) VALUES (?, ?, ?, ?)",
            (name, password, max_players, host_id)
        )
        conn.commit()
        room_id = cursor.lastrowid
        conn.close()
        return room_id

    @staticmethod
    def get_by_id(room_id):
        conn = get_db()
        room = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
        conn.close()
        return dict(room) if room else None

    @staticmethod
    def get_all_active():
        conn = get_db()
        rooms = conn.execute("SELECT * FROM rooms WHERE status != 'finished' ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rooms]

    @staticmethod
    def update_status(room_id, status):
        conn = get_db()
        conn.execute("UPDATE rooms SET status = ? WHERE id = ?", (status, room_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(room_id):
        conn = get_db()
        conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
        conn.commit()
        conn.close()


class RoomPlayer:
    @staticmethod
    def add_player(room_id, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO room_players (room_id, user_id) VALUES (?, ?)",
            (room_id, user_id)
        )
        conn.commit()
        rp_id = cursor.lastrowid
        conn.close()
        return rp_id

    @staticmethod
    def remove_player(room_id, user_id):
        conn = get_db()
        conn.execute("DELETE FROM room_players WHERE room_id = ? AND user_id = ?", (room_id, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_players_in_room(room_id):
        conn = get_db()
        query = """
            SELECT u.id, u.username, rp.is_ready 
            FROM room_players rp
            JOIN users u ON rp.user_id = u.id
            WHERE rp.room_id = ?
        """
        players = conn.execute(query, (room_id,)).fetchall()
        conn.close()
        return [dict(p) for p in players]

    @staticmethod
    def set_ready(room_id, user_id, is_ready):
        conn = get_db()
        conn.execute(
            "UPDATE room_players SET is_ready = ? WHERE room_id = ? AND user_id = ?",
            (is_ready, room_id, user_id)
        )
        conn.commit()
        conn.close()
