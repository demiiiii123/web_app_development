from flask import Flask
from flask_socketio import SocketIO
import os

# 初始化 SocketIO
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
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

    from app.routes import auth_routes, lobby_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(lobby_routes.bp)

    return app

app = create_app()

if __name__ == '__main__':
    # 使用 socketio.run 啟動伺服器，支援 WebSocket
    socketio.run(app, debug=True)
