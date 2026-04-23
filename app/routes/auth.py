from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    """
    首頁/登入頁面
    - 若 session 中已有 user_id，重導向到 /lobby
    - 否則渲染 auth/login.html
    """
    pass

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    處理訪客登入
    - 接收表單 username
    - 建立 User 資料 (is_guest=True)
    - 儲存 user_id 到 session
    - 重導向到 /lobby
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    登出
    - 清除 session
    - 重導向到 /
    """
    pass
