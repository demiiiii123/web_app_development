from flask import Blueprint, render_template, request, redirect, url_for, session, flash

room_bp = Blueprint('room', __name__)

@room_bp.route('/create', methods=['POST'])
def create_room():
    """
    建立新房間
    - 驗證登入
    - 呼叫 Room.create(host_id)
    - 將房主自己加入房間 RoomPlayer.join_room()
    - 重導向到 /room/<invite_code>
    """
    pass

@room_bp.route('/join', methods=['POST'])
def join_room():
    """
    加入房間
    - 接收表單 invite_code
    - 驗證房間是否存在且未滿
    - 呼叫 RoomPlayer.join_room()
    - 重導向到 /room/<invite_code>
    """
    pass

@room_bp.route('/<invite_code>', methods=['GET'])
def waiting_room(invite_code):
    """
    房間等待區
    - 驗證使用者是否在此房間內
    - 取得房內所有玩家資料
    - 渲染 lobby/room.html
    """
    pass

@room_bp.route('/<invite_code>/leave', methods=['POST'])
def leave_room(invite_code):
    """
    離開房間
    - 呼叫 RoomPlayer.leave_room()
    - 若是房主離開，可能需要解散房間或轉讓房主
    - 重導向到 /lobby
    """
    pass

@room_bp.route('/<invite_code>/start', methods=['POST'])
def start_game(invite_code):
    """
    開始遊戲
    - 驗證是否為房主
    - 更改房間狀態 Room.update_status(playing)
    - 重導向到 /game/<invite_code>
    """
    pass
