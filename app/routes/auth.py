from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('lobby.index'))
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if not username or len(username.strip()) == 0:
        flash("請輸入有效的暱稱", "error")
        return redirect(url_for('auth.index'))
        
    user = User.create(username.strip(), is_guest=True)
    if user:
        session['user_id'] = user.id
        return redirect(url_for('lobby.index'))
        
    flash("登入失敗，請稍後再試", "error")
    return redirect(url_for('auth.index'))

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.index'))
