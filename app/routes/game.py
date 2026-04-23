from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.models.room import Room, RoomPlayer
from app.models.game import GameHistory
from app.models.user import User

game_bp = Blueprint('game', __name__)

@game_bp.route('/<invite_code>', methods=['GET'])
def game_view(invite_code):
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    room = Room.get_by_invite_code(invite_code)
    if not room or room.status != 'playing':
        return redirect(url_for('room.waiting_room', invite_code=invite_code))
        
    players = RoomPlayer.get_players_in_room(room.id)
    is_in_room = any(p['user_id'] == session['user_id'] for p in players)
    if not is_in_room:
        return redirect(url_for('lobby.index'))
        
    current_user = User.get_by_id(session['user_id'])
    return render_template('game/index.html', room=room, players=players, current_user=current_user)

@game_bp.route('/api/<invite_code>/status', methods=['GET'])
def game_status(invite_code):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    room = Room.get_by_invite_code(invite_code)
    if not room:
        return jsonify({"error": "Room not found"}), 404
        
    players = RoomPlayer.get_players_in_room(room.id)
    return jsonify({
        "status": room.status,
        "players": players
    })

@game_bp.route('/api/<invite_code>/play', methods=['POST'])
def game_play(invite_code):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    room = Room.get_by_invite_code(invite_code)
    if not room or room.status != 'playing':
        return jsonify({"error": "Invalid room state"}), 400
        
    user_id = session['user_id']
    data = request.json
    action_type = data.get('action_type')
    
    # 通用的 MVP 得分邏輯
    if action_type == 'score':
        points = data.get('value', 1)
        RoomPlayer.update_score(room.id, user_id, points)
        
        # 檢查是否有人獲勝 (例如先達到 50 分)
        players = RoomPlayer.get_players_in_room(room.id)
        winner = next((p for p in players if p['score'] >= 50), None)
        
        if winner:
            Room.update_status(room.id, 'finished')
            GameHistory.create(room.id, winner['user_id'])
            return jsonify({"success": True, "game_over": True, "winner_id": winner['user_id']})
            
        return jsonify({"success": True, "game_over": False})
        
    return jsonify({"error": "Unknown action"}), 400
