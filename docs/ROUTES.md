# 路由設計文件 (API & Routes)

本文件依據 PRD 與 FLOWCHART，定義了系統中所有的網址路徑、HTTP 方法、對應的處理邏輯與渲染的頁面。
我們會使用 Flask 的 **Blueprint** 將路由分為四大模組：`auth`, `lobby`, `room`, `game`。

## 1. 路由總覽表格

### Auth 模組 (身分驗證)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁/登入頁 | GET | `/` | `auth/login.html` | 若已登入則重導向 `/lobby`，否則顯示首頁/訪客登入表單 |
| 登入處理 | POST | `/login` | — | 接收使用者輸入的暱稱，註冊並設定 Session，重導向 `/lobby` |
| 登出 | GET | `/logout` | — | 清除 Session，重導向 `/` |

### Lobby 模組 (大廳)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 大廳主頁 | GET | `/lobby` | `lobby/index.html` | 顯示玩家資訊、建立房間與加入房間的按鈕 |
| 個人戰績 | GET | `/profile` | `lobby/profile.html` | 顯示該名玩家的歷史戰績與分數 |

### Room 模組 (房間管理)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 建立房間 | POST | `/room/create` | — | 建立新房間，取得邀請碼後，重導向 `/room/<invite_code>` |
| 加入房間 | POST | `/room/join` | — | 接收邀請碼，驗證後重導向 `/room/<invite_code>` |
| 房間等待區 | GET | `/room/<invite_code>` | `lobby/room.html` | 顯示房內目前玩家列表。若是房主，可看見「開始遊戲」按鈕 |
| 離開房間 | POST | `/room/<invite_code>/leave` | — | 將玩家從房間移除，重導向 `/lobby` |
| 開始遊戲 | POST | `/room/<invite_code>/start` | — | 房主專用，更改房間狀態為 playing，重導向 `/game/<invite_code>` |

### Game 模組 (遊戲邏輯)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 遊戲主畫面 | GET | `/game/<invite_code>` | `game/index.html` | 遊戲介面。透過前端 JS 呼叫下方 API 進行更新 |
| 取得狀態 API | GET | `/api/game/<invite_code>/status` | — (回傳 JSON) | 前端輪詢用，回傳最新分數與狀態 |
| 執行操作 API | POST | `/api/game/<invite_code>/play` | — (回傳 JSON) | 玩家出牌或動作時呼叫，後端驗證並更新分數 |

---

## 2. 每個路由的詳細說明

### Auth 路由
*   `POST /login`
    *   **輸入**：表單欄位 `username`
    *   **處理邏輯**：呼叫 `User.create(username, is_guest=True)`，將返回的 `user.id` 存入 Flask Session。
    *   **輸出**：`redirect('/lobby')`

### Room 路由
*   `POST /room/join`
    *   **輸入**：表單欄位 `invite_code`
    *   **處理邏輯**：查詢房間是否存在，若存在則呼叫 `RoomPlayer.join_room()`。
    *   **錯誤處理**：若房間不存在或客滿，`flash()` 錯誤訊息並重新渲染 `lobby/index.html`。
    *   **輸出**：`redirect('/room/<invite_code>')`

### Game API
*   `POST /api/game/<invite_code>/play`
    *   **輸入**：JSON 包含 `action_type`, `value` 等操作細節。
    *   **處理邏輯**：呼叫遊戲核心邏輯驗證動作，呼叫 `RoomPlayer.update_score()`，若達成勝利條件則呼叫 `GameHistory.create()`。
    *   **輸出**：回傳 `{ "success": true, "new_score": ... }`。

---

## 3. Jinja2 模板清單

所有的模板檔案會建立在 `app/templates/` 目錄下：

1.  **`base.html`**：全域共用版型（包含 HTML 骨架、載入 Bootstrap / 自訂 CSS / JS，以及 Header 導覽列）。
2.  **`auth/login.html`**：繼承 `base.html`，純粹的登入/設定訪客暱稱畫面。
3.  **`lobby/index.html`**：繼承 `base.html`，大廳畫面。
4.  **`lobby/profile.html`**：繼承 `base.html`，個人成就畫面。
5.  **`lobby/room.html`**：繼承 `base.html`，房間等待區畫面。
6.  **`game/index.html`**：**可能不繼承** `base.html`，因為遊戲畫面通常需要佔滿全螢幕且擁有專屬的沉浸式 CSS 與特效，會獨立撰寫完整的 HTML 結構。
