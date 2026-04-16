# 假設使用 flask_socketio 中的 socketio

def setup_sockets(socketio):
    @socketio.on('join')
    def on_join(data):
        """
        處理玩家連線，將玩家的 Socket 加入指定的房間頻道 (Room)。
        廣播給同房玩家：某人已加入。
        """
        pass

    @socketio.on('leave')
    def on_leave(data):
        """
        處理玩家斷線或離開網頁，將玩家從該頻道移除。
        廣播離開訊息。
        """
        pass

    @socketio.on('chat_msg')
    def handle_chat_message(data):
        """
        接收文字訊息，廣播給全房間的玩家顯示於聊天室內容中。
        """
        pass

    @socketio.on('game_action')
    def handle_game_action(data):
        """
        處理核心遊戲操作指令（例如：玩家點選九宮格、出牌等）。
        驗證合法性並更新遊戲狀態後，廣播新盤面。
        """
        pass
