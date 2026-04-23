# 系統架構文件 (Architecture Design)

這份文件基於 `docs/PRD.md` 中定義的桌遊系統需求，規劃系統的技術架構、資料夾結構與核心元件的互動關係。

## 1. 技術架構說明

本系統主要依循 **MVC (Model-View-Controller)** 設計模式，確保邏輯、資料與呈現層面清楚分離。

*   **選用技術與原因**：
    *   **後端框架**：**Python + Flask**。Flask 是一個輕量、靈活的微框架，非常適合快速開發與建置 MVP 原型。
    *   **模板引擎**：**Jinja2**。內建於 Flask，可直接將後端資料注入 HTML 模板，無需建立複雜的前後端分離架構，降低初期開發門檻。
    *   **資料庫**：**SQLite** (建議搭配 SQLAlchemy ORM)。輕便、無須額外架設資料庫伺服器，資料直接存在本地檔案中，非常適合中小型專案與開發階段使用。
*   **MVC 模式在此專案的對應**：
    *   **Model (模型)**：負責定義資料庫結構（如玩家 `User`、房間 `Room`、遊戲紀錄 `GameHistory`）與處理資料的存取邏輯。
    *   **View (視圖)**：負責呈現使用者介面。在這裡就是 **Jinja2 HTML 模板**與前端靜態資源（CSS/JS）。
    *   **Controller (控制器)**：負責接收瀏覽器的請求並進行邏輯判斷。在這裡即為 **Flask 的 Routes (路由)**，它會呼叫 Model 取得資料，再交給 View 進行渲染回傳。

---

## 2. 專案資料夾結構

為了保持專案的可維護性，我們將採用功能模組化的資料夾結構：

```text
web_app_development/
├── app/                  # 應用程式主目錄 (Flask 核心)
│   ├── __init__.py       # 初始化 Flask 應用與資料庫連線設定
│   ├── models/           # Model：資料庫模型
│   │   ├── user.py       # 處理帳號、訪客、成就相關
│   │   ├── room.py       # 處理大廳、房間連線狀態
│   │   └── game.py       # 處理桌遊計分與仲裁邏輯
│   ├── routes/           # Controller：Flask 路由
│   │   ├── auth.py       # 處理登入/註冊/訪客身分
│   │   ├── lobby.py      # 處理建立/加入房間
│   │   └── game.py       # 處理遊戲內行為與即時互動
│   ├── templates/        # View：Jinja2 HTML 模板
│   │   ├── base.html     # 共用版型 (Header/Footer)
│   │   ├── auth/         # 登入與註冊頁面
│   │   ├── lobby/        # 大廳與房間頁面
│   │   └── game/         # 遊戲主畫面與動態計分板
│   └── static/           # 靜態資源
│       ├── css/          # 樣式表 (負責沉浸式視覺)
│       ├── js/           # 前端互動腳本 (處理即時狀態更新)
│       └── img/          # 遊戲素材、成就徽章
├── docs/                 # 專案文件 (如 PRD.md, ARCHITECTURE.md)
├── instance/             # 存放本地特定檔案
│   └── database.db       # SQLite 資料庫檔案
├── .gitignore            # Git 忽略清單 (忽略虛擬環境與 database.db 等)
├── requirements.txt      # Python 第三方套件依賴清單
└── app.py                # 系統啟動入口檔案
```

---

## 3. 元件關係圖

以下圖表說明了使用者操作時，資料如何在系統各元件之間流動：

```mermaid
flowchart TD
    Browser[瀏覽器 Browser \n (玩家操作介面)]
    
    subgraph Flask 應用程式 (Server端)
        Controller[Flask Route \n Controller]
        View[Jinja2 Template \n View]
        Model[Models \n ORM]
    end
    
    DB[(SQLite 資料庫)]
    
    %% 互動流程
    Browser -- "1. 發送請求 \n (HTTP GET/POST)" --> Controller
    Controller -- "2. 查詢/寫入資料 \n (如: 驗證房間密碼)" --> Model
    Model -- "3. 資料庫存取" --> DB
    DB -- "回傳查詢結果" --> Model
    Model -- "回傳 Python 物件" --> Controller
    Controller -- "4. 傳遞資料 \n (如: 將分數傳給畫面)" --> View
    View -- "5. 渲染帶有資料的 HTML 頁面" --> Browser
```

---

## 4. 關鍵設計決策

1.  **採用伺服器端渲染 (SSR) 而非前後端分離**
    *   **原因**：考量到開發時程與降低技術複雜度，不導入 React/Vue 等框架。使用 Flask + Jinja2 直接渲染頁面，能最快產出 MVP。畫面中的小範圍互動（如即時分數跳動）則透過 Vanilla JS (原生 JavaScript) 處理即可。
2.  **即時互動機制的選擇**
    *   **決策**：桌遊系統極度依賴「即時性」（如動態計分、輪到誰的回合）。初期開發階段若不熟悉 WebSocket，可先利用前端 JavaScript 的 `setInterval()` 定期向後端請求更新（Long/Short Polling）。但強烈建議後續導入 `Flask-SocketIO`，以達成真正的雙向即時通訊，符合 PRD 中提到的延遲 < 1秒 需求。
3.  **遊戲邏輯的抽象化**
    *   **決策**：為了未來的擴充性（Nice to have: 擴充更多款不同的桌遊），路由 `routes/game.py` 與 `models/game.py` 在設計時，應該將「房間管理/連線狀態」與「特定桌遊的規則（仲裁邏輯）」拆分開來。建立一個基礎的 Game 類別，後續不同的桌遊可以繼承並實作各自的計分與仲裁邏輯。
