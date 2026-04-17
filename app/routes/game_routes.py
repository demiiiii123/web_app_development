from flask import request, render_template, redirect, url_for, session
from . import game_bp

@game_bp.route('/room/<int:room_id>', methods=['GET'])
def view_room(room_id):
    """
    驗證登入，並檢查使用者是否在 RoomPlayer 名單中。
    渲染房間介面 (room.html)，以供前端建立 WebSocket 即時互動。
    """
    pass

@game_bp.route('/room/<int:room_id>/join', methods=['POST'])
def join_room(room_id):
    """
    接收密碼驗證 (如需)，並檢查房間人數是否已滿。
    成功則將玩家加入 RoomPlayer，隨後重導向 /room/<id>。
    """
    pass

@game_bp.route('/room/<int:room_id>/leave', methods=['POST'])
def leave_room(room_id):
    """
    清除該玩家的 RoomPlayer 紀錄。
    若該玩家為房主，處理房主移交或解散房間。重導向 /lobby。
    """
    pass
