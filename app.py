from flask import Flask
from flask_socketio import SocketIO
import os

# 初始化 SocketIO
socketio = SocketIO()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    # 載入設定參數
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret_key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')

    # 確保 instance 資料夾存在（用來存放 SQLite 資料庫檔案）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 將 SocketIO 綁定到 app 上
    socketio.init_app(app)

    from app.routes import auth, lobby, room, game
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(lobby.lobby_bp)
    app.register_blueprint(room.room_bp, url_prefix='/room')
    app.register_blueprint(game.game_bp, url_prefix='/game')

    return app

app = create_app()

if __name__ == '__main__':
    # 使用 socketio.run 啟動伺服器，支援 WebSocket
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
