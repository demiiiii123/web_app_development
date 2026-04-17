from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import user

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET'])
def index():
    """首頁：未登入顯示登入頁面，已登入導向大廳"""
    if 'user_id' in session:
        return redirect(url_for('lobby.index'))
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """處理會員註冊請求"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 進行基本的輸入驗證
        if not username or not password:
            flash('請輸入帳號與密碼', 'danger')
            return redirect(url_for('auth.index'))
        
        # 檢查是否已存在
        if user.get_by_username(username):
            flash('此帳號已存在，請更換一個名稱', 'warning')
            return redirect(url_for('auth.index'))

        # 寫入資料庫
        password_hash = generate_password_hash(password)
        new_id = user.create({'username': username, 'password_hash': password_hash})
        
        if new_id:
            flash('註冊成功！請直接登入', 'success')
        else:
            flash('註冊時發生系統錯誤', 'danger')
            
        return redirect(url_for('auth.index'))
    
    return render_template('index.html')

@bp.route('/login', methods=['POST'])
def login():
    """處理會員登入請求"""
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('請輸入帳號與密碼', 'danger')
        return redirect(url_for('auth.index'))
    
    # 驗證身分
    u = user.get_by_username(username)
    if u and check_password_hash(u['password_hash'], password):
        session['user_id'] = u['id']
        session['username'] = u['username']
        flash('登入成功！歡迎進入遊戲大廳', 'success')
        return redirect(url_for('lobby.index'))
    else:
        flash('帳號或密碼錯誤，請重新輸入', 'danger')
        return redirect(url_for('auth.index'))

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """處理登出請求"""
    session.clear()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.index'))
