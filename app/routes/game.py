from flask import Blueprint, render_template, request, jsonify, session

game_bp = Blueprint('game', __name__)

@game_bp.route('/<invite_code>', methods=['GET'])
def game_view(invite_code):
    """
    遊戲主畫面
    - 驗證使用者是否在該房間，且房間狀態為 playing
    - 渲染 game/index.html (包含前端 JS)
    """
    pass

@game_bp.route('/api/<invite_code>/status', methods=['GET'])
def game_status(invite_code):
    """
    [API] 取得當前遊戲狀態
    - 查詢房間內所有玩家的分數與準備狀態
    - 查詢當前回合資訊
    - 回傳 JSON
    """
    pass

@game_bp.route('/api/<invite_code>/play', methods=['POST'])
def game_play(invite_code):
    """
    [API] 執行玩家動作
    - 接收前端 JSON (動作類型、參數)
    - 遊戲核心邏輯仲裁：是否合法？是否得分？是否分出勝負？
    - 若結束，更新 Room 狀態為 finished，建立 GameHistory
    - 回傳 JSON (成功與否、最新狀態)
    """
    pass
