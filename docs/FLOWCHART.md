# 流程圖設計文件 (Flowchart)

本文件基於線上桌遊系統的需求說明 (PRD) 與系統架構 (ARCHITECTURE) 產出，以視覺化的方式呈現使用者的操作動線及系統的資料傳遞流程，確保前後端開發對齊邏輯。

---

## 1. 使用者流程圖 (User Flow)

此圖描述使用者從一開始打開網站後，直到註冊登入、瀏覽大廳、加入房間遊玩到最終查看戰績的一系列操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Index[首頁 / 登入頁]
    
    Index -- 無帳號 --> Register[點擊註冊]
    Register --> RegisterForm[填寫註冊表單]
    RegisterForm -- 成功註冊 --> Index
    
    Index -- 有帳號 --> Login[輸入帳密登入]
    Login -- 驗證失敗 --> Index
    Login -- 驗證成功 --> Lobby[進入遊戲大廳]
    
    Lobby --> LobbyDecisions{選擇操作}
    
    LobbyDecisions -- 建立房間 --> CreateRoom[填寫房間設定與人數限制]
    CreateRoom --> Room[進入專屬房間]
    
    LobbyDecisions -- 瀏覽與加入 --> JoinRoom[選擇房間並輸入密碼]
    JoinRoom -- 密碼正確 --> Room
    JoinRoom -- 錯誤 --> Lobby
    
    LobbyDecisions -- 查看戰績 --> Profile[個人中心：查看勝率與排行榜]
    Profile --> Lobby
    
    Room --> RoomDecisions{房間內互動}
    RoomDecisions -- 即時通訊 --> Chat[於聊天室發送文字] --> RoomDecisions
    RoomDecisions -- 準備就緒 --> Ready[點擊準備] --> RoomDecisions
    
    RoomDecisions -- 房主開始遊戲 --> GameStart[進入遊戲階段]
    GameStart --> GamePlay[輪流進行遊戲操作]
    GamePlay -- 遊戲進行中 --> GamePlay
    GamePlay -- 滿足分出勝負條件 --> GameOver[顯示結算畫面與積分更新] --> Room
    
    RoomDecisions -- 離開 --> Leave[退出房間回到大廳] --> Lobby
```

---

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述 MVP 中最重要的核心邏輯之一：**使用者從大廳點擊「建立新房間」到資料庫建立資料，並順利進入房間** 的系統資料流通訊完整過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Flask as Flask Controller (routes)
    participant Model as Database Model (Room)
    participant DB as SQLite 資料庫

    User->>Browser: 填寫建房表單並點擊「建立」
    Browser->>Flask: POST /room/create (表單資料: 房間名, 密碼等)
    Flask->>Flask: 檢查使用者 Session 是否具備登入資格
    
    alt 尚未登入或權限不足
        Flask-->>Browser: 拒絕存取，HTTP 302 導回首頁
    else 驗證成功
        Flask->>Model: 呼叫 Room.create(...)
        Model->>DB: 執行 INSERT INTO rooms ...
        DB-->>Model: 回傳新建立的 Room ID
        Model-->>Flask: 取得剛建立的房間實例
        Flask-->>Browser: HTTP 302 Redirect 到 /room/<RoomID>
        
        Note over Browser, Flask: 進入房間頁面並建立即時連線
        Browser->>Flask: GET /room/<RoomID>
        Flask-->>Browser: 透過 Jinja2 回傳 room.html (含房間現狀資料)
        Browser->>Flask: 解析完 HTML，連線 WebSocket (emit 'join')
        Flask->>Model: 更新玩家狀態與 Socket 綁定
        Model->>DB: UPDATE rooms SET players = ...
        DB-->>Model: 成功
        Model-->>Flask: 成功
        Flask-->>Browser: 推播推播更新事件 (broadcast 'room_update') 給全房玩家
    end
```

---

## 3. 功能清單對照表

統整系統所涵蓋的核心功能及其對應存取路徑，提供給前端介接與後端實作時參考。

| 功能區塊 | 子功能 | URL 路徑 | HTTP 方法 / WebSocket事件 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **會員管理** | 註冊帳號 | `/register` | GET, POST | GET: 註冊頁，POST: 寫入帳號資料 |
| | 會員登入 | `/login` | GET, POST | POST: 驗證帳密並寫入 Session |
| | 會員登出 | `/logout` | GET | 清除 Session 並導回首頁 |
| | 個人中心 | `/profile` | GET | 顯示目前登入者的詳細戰績及排行榜 |
| **大廳與房間** | 瀏覽大廳 | `/lobby` | GET | 查詢所有啟用的房間清單 |
| | 建立房間 | `/room/create` | POST | 接收建立參數並寫入資料庫 |
| | 加入房間 | `/room/join/<id>`| POST | 驗證密碼後，將該房資料與玩家結合 |
| | 房間畫面 | `/room/<id>` | GET | 渲染特定房間之 UI 介面，準備建立 Socket |
| **即時遊戲機制**| 加入房間頻道 | `/room/<id>` | `emit('join')` | 處理玩家 Socket 加入 SocketIO 指定的房頻道 |
| | 即時通訊 | `/room/<id>` | `emit('chat_msg')` | 傳送訊息並由 Flask 透過 broadcast 推送給所有房客 |
| | 遊戲動作指令 | `/room/<id>` | `emit('game_action')` | 包含出牌、下棋等指令，驗證邏輯後推播更新盤面 |
