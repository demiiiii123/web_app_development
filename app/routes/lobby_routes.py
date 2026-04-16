from flask import request, render_template, redirect, url_for, session
from . import lobby_bp

@lobby_bp.route('/lobby', methods=['GET'])
def lobby():
    """
    驗證登入。
    呼叫 Room.get_all_active() 取得活躍房間列表，並渲染大廳頁面。
    """
    pass

@lobby_bp.route('/room/create', methods=['POST'])
def create_room():
    """
    接收建房表單 (名稱, 密碼, 人數)。
    建立房間並將自己加入 RoomPlayer，成功後重導向 /room/<id>。
    """
    pass
