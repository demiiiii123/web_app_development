from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.user import User
from app.models.game import GameHistory

lobby_bp = Blueprint('lobby', __name__)

@lobby_bp.route('/lobby', methods=['GET'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    user = User.get_by_id(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('auth.index'))
        
    return render_template('lobby/index.html', current_user=user)

@lobby_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    user = User.get_by_id(session['user_id'])
    histories = GameHistory.get_user_histories(user.id)
    
    return render_template('lobby/profile.html', current_user=user, histories=histories)
