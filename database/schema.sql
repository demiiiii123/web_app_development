DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;

-- 會員資料表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    wins INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 遊戲房間資料表
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT,
    host_id INTEGER NOT NULL,
    status TEXT DEFAULT 'waiting', -- waiting, playing, closed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users (id)
);
