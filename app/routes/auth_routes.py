from flask import request, render_template, redirect, url_for, session
from . import auth_bp

@auth_bp.route('/', methods=['GET'])
def index():
    """
    檢查 Session 中有無 user_id。
    有則導向 /lobby，無則顯示首頁 (登入與註冊表單)。
    """
    pass

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    接收註冊表單，驗證密碼相符與帳號是否重複。
    加密密碼後建立 User，成功導回到首頁。
    """
    pass

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    接收登入表單，驗證密碼。
    成功則將 user_id 寫入 Session，導向 /lobby。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    清除 Session 中的 user_id 並導回首頁。
    """
    pass

@auth_bp.route('/profile', methods=['GET'])
def profile():
    """
    驗證登入。
    顯示個人勝率、場次、歷史紀錄，以及全服排行榜。
    """
    pass
