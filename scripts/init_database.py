import sqlite3
import os

db_path = 'public/trading.db'

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 建立任務資料表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'backlog',
        priority TEXT DEFAULT 'medium',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 檢查是否已有資料，若無則從 KANBAN.md 導入初始資料
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        initial_tasks = [
            ('OCR 截圖解析', '上傳截圖後自動識別 Setup 狀態', 'backlog', 'high'),
            ('自動短片生成', '將大賺交易生成短影音素材', 'backlog', 'medium'),
            ('TradingView 圖表整合', '在網頁顯示進出場 K 線圖', 'todo', 'high'),
            ('架構標準化整合', '統一所有頁面的 Sidepanel', 'inprogress', 'medium')
        ]
        cursor.executemany('INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)', initial_tasks)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_db()
