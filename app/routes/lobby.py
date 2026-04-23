from flask import Blueprint, render_template, session, redirect, url_for

lobby_bp = Blueprint('lobby', __name__)

@lobby_bp.route('/lobby', methods=['GET'])
def index():
    """
    大廳主頁
    - 需驗證是否登入（檢查 session）
    - 顯示玩家基本資料
    - 提供建立房間、加入房間的按鈕與表單
    - 渲染 lobby/index.html
    """
    pass

@lobby_bp.route('/profile', methods=['GET'])
def profile():
    """
    個人戰績與成就
    - 需驗證是否登入
    - 查詢該玩家的歷史戰績
    - 渲染 lobby/profile.html
    """
    pass
