from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.room import Room, RoomPlayer

room_bp = Blueprint('room', __name__)

@room_bp.route('/create', methods=['POST'])
def create_room():
    if 'user_id' not in session:
        flash("請先登入或輸入暱稱", "error")
        return redirect(url_for('auth.index'))
    
    user_id = session['user_id']
    room = Room.create(host_id=user_id)
    if room:
        RoomPlayer.join_room(room.id, user_id)
        return redirect(url_for('room.waiting_room', invite_code=room.invite_code))
    
    flash("建立房間失敗，請稍後再試", "error")
    return redirect(url_for('lobby.index'))

@room_bp.route('/join', methods=['POST'])
def join_room():
    if 'user_id' not in session:
        flash("請先登入或輸入暱稱", "error")
        return redirect(url_for('auth.index'))
        
    invite_code = request.form.get('invite_code')
    if not invite_code:
        flash("請輸入邀請碼", "error")
        return redirect(url_for('lobby.index'))
        
    room = Room.get_by_invite_code(invite_code)
    if not room:
        flash("找不到該房間", "error")
        return redirect(url_for('lobby.index'))
        
    if room.status != 'waiting':
        flash("該房間遊戲已開始或結束", "error")
        return redirect(url_for('lobby.index'))
        
    user_id = session['user_id']
    RoomPlayer.join_room(room.id, user_id)
    return redirect(url_for('room.waiting_room', invite_code=room.invite_code))

@room_bp.route('/<invite_code>', methods=['GET'])
def waiting_room(invite_code):
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    room = Room.get_by_invite_code(invite_code)
    if not room:
        flash("房間不存在", "error")
        return redirect(url_for('lobby.index'))
        
    players = RoomPlayer.get_players_in_room(room.id)
    # 確認當前使用者是否在房間內
    is_in_room = any(p['user_id'] == session['user_id'] for p in players)
    if not is_in_room:
        flash("您不在該房間內", "error")
        return redirect(url_for('lobby.index'))
        
    # 如果已經開始，直接導向遊戲畫面
    if room.status == 'playing':
        return redirect(url_for('game.game_view', invite_code=invite_code))
        
    is_host = (room.host_id == session['user_id'])
    return render_template('lobby/room.html', room=room, players=players, is_host=is_host)

@room_bp.route('/<invite_code>/leave', methods=['POST'])
def leave_room(invite_code):
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    room = Room.get_by_invite_code(invite_code)
    if room:
        RoomPlayer.leave_room(room.id, session['user_id'])
        # 簡單處理：若房主離開，房間可能需要解散（MVP暫不處理轉移）
    return redirect(url_for('lobby.index'))

@room_bp.route('/<invite_code>/start', methods=['POST'])
def start_game(invite_code):
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    room = Room.get_by_invite_code(invite_code)
    if room and room.host_id == session['user_id']:
        Room.update_status(room.id, 'playing')
        return redirect(url_for('game.game_view', invite_code=invite_code))
        
    flash("只有房主可以開始遊戲", "error")
    return redirect(url_for('room.waiting_room', invite_code=invite_code))
