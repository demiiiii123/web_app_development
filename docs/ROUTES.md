# 路由與頁面設計 (Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `index.html` | 首頁，未登入顯示登入與註冊表單；已登入導向 `/lobby` |
| 註冊 | POST | `/register` | — | 接收表單並建立 User，成功導向 `/`，失敗重導向 `/` 並顯示錯誤 |
| 登入 | POST | `/login` | — | 接收表單驗證密碼，成功寫入 Session 並導向 `/lobby` |
| 登出 | GET | `/logout` | — | 清除 Session 並導向 `/` |
| 個人中心 | GET | `/profile` | `profile.html` | 顯示個人勝率、場次與全服排行榜 |
| 遊戲大廳 | GET | `/lobby` | `lobby.html` | 顯示等待中的房間清單，可點擊加入或開房 |
| 建立房間 | POST | `/room/create` | — | 接收建房表單，存入 DB 並重導向 `/room/<id>` |
| 加入房間 | POST | `/room/<id>/join`| — | 驗證密碼(如需)與人數限制，成功寫入 `room_players` 後導向 `/room/<id>` |
| 房間/遊戲畫面 | GET | `/room/<id>` | `room.html` | 渲染房間介面，供前端建立 WebSocket 進行實時互動 |
| 退出房間 | POST | `/room/<id>/leave`| — | 處理人員離開邏輯後，重導向 `/lobby` |

## 2. 每個路由的詳細說明

### Auth (`auth_routes.py`)
- **`GET /`**
  - 輸入：無
  - 邏輯：檢查 Session 中有無 `user_id`，有則導向 `/lobby`，無則顯示首頁
  - 輸出：渲染 `index.html`
- **`POST /register`**
  - 輸入：表單 `username`, `password`, `confirm_password`
  - 邏輯：驗證密碼相符與帳號是否重複，加密後呼叫 `User.create(...)`
  - 輸出：成功導向 `/` 顯示成功訊息，失敗重導向 `/` 提示錯誤
- **`POST /login`**
  - 輸入：表單 `username`, `password`
  - 邏輯：呼叫 `User.get_by_username()` 查詢，驗證 Hash 密碼。成功將 `user_id` 寫入 Session
  - 輸出：成功導向 `/lobby`，失敗重導向 `/` 提示錯誤
- **`GET /logout`**
  - 邏輯：移除 Session 內之 `user_id`
  - 輸出：重導向 `/`
- **`GET /profile`**
  - 邏輯：檢查登入狀態。利用 `User.get_by_id()` 和 `GameHistory.get_by_user()` 抓取資料，並以 `User.get_all()` 產生排行榜
  - 輸出：渲染 `profile.html`

### Lobby (`lobby_routes.py`)
- **`GET /lobby`**
  - 邏輯：驗證登入。呼叫 `Room.get_all_active()` 取得房間列表，渲染大廳頁面
  - 輸出：渲染 `lobby.html`
- **`POST /room/create`**
  - 輸入：表單 `name`, `password`, `max_players`
  - 邏輯：以當前 user_id 為 host，呼叫 `Room.create(...)` 並將自己加入 `RoomPlayer`
  - 輸出：成功導向 `/room/<id>`

### Game (`game_routes.py`)
- **`POST /room/<id>/join`**
  - 輸入：表單 `password` (選擇性)
  - 邏輯：驗證房間狀態非 finished、人數未滿、密碼正確。呼叫 `RoomPlayer.add_player()`
  - 輸出：成功重導 `/room/<id>`，失敗導回 `/lobby` 並攜帶錯誤
- **`GET /room/<id>`**
  - 邏輯：驗證登入及使用者是否在 `RoomPlayer` 名單。取得 `Room` 與在線玩家清單。
  - 輸出：渲染 `room.html`
- **`POST /room/<id>/leave`**
  - 邏輯：清除該玩家的 `RoomPlayer` 紀錄。若為房主則解散房間或移交房主。
  - 輸出：導向 `/lobby`

### Socket Events (`socket_events.py`)
- **`join` / `leave`**：將連接加入/退出指定的 SocketIO Room
- **`chat_msg`**：接收文字，廣播給全房間玩家
- **`game_action`**：接收玩家的遊戲核心操作（例如：點擊棋盤），驗證是否符合規則並更新狀態後廣播新盤面給全房。

## 3. Jinja2 模板清單

- `templates/base.html`: 共同樣板，包含 Navbar、基礎 CSS 與 Bootstrap/Tailwind CDN
- `templates/index.html`: 繼承 `base.html`，放置系統簡介與登入/註冊 Tabs
- `templates/lobby.html`: 繼承 `base.html`，動態列出房間卡片，並提供新增房間的 Modal 或區塊
- `templates/profile.html`: 繼承 `base.html`，展示玩家勝率、過去紀錄列表及全服排行榜
- `templates/room.html`: 繼承 `base.html`，(分為等待狀態與遊戲開始狀態)，包含聊天室區塊與右側遊戲盤面區塊
