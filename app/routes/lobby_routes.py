from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import room

# 設定 url_prefix 讓這組路由都在 /lobby 底下
bp = Blueprint('lobby', __name__, url_prefix='/lobby')

@bp.route('/')
def index():
    """遊戲大廳首頁：列出所有可加入的房間"""
    # 確認權限 (登入保護)
    if 'user_id' not in session:
        flash('請先登入會員以進入大廳', 'danger')
        return redirect(url_for('auth.index'))
        
    # 取出所有房間清單
    rooms = room.get_all()
    return render_template('lobby.html', rooms=rooms, current_username=session.get('username'))

@bp.route('/create', methods=['POST'])
def create_room():
    """處理新增房間請求"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    name = request.form.get('name')
    password = request.form.get('password', '') # 選填
    
    if not name:
        flash('請輸入房間名稱才能建立', 'danger')
        return redirect(url_for('lobby.index'))
        
    new_id = room.create({
        'name': name,
        'host_id': session['user_id'],
        'password': password
    })
    
    if new_id:
        flash('順利建立房間！', 'success')
        # Todo: 重導向到 game_routes (房間頁面)
        # return redirect(url_for('game.room_view', room_id=new_id))
        return redirect(url_for('lobby.index')) 
    else:
        flash('建立房間失敗，請稍後再試', 'danger')
        return redirect(url_for('lobby.index'))
