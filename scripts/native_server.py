import http.server
import socketserver
import json
import sqlite3
import os

# 強制路徑與連接埠
PORT = 80
BASE_DIR = '/home/aliple/.openclaw/workspace/public'
DB_PATH = os.path.join(BASE_DIR, 'trading.db')

class UnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API 處理
        if self.path == '/api/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, status, priority FROM tasks')
            tasks = [{"id": r[0], "title": r[1], "description": r[2], "status": r[3], "priority": r[4]} for r in cursor.fetchall()]
            conn.close()
            self.wfile.write(json.dumps(tasks).encode())
        else:
            # 靜態網頁處理
            os.chdir(BASE_DIR)
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/tasks':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)',
                           (data['title'], data.get('description', ''), data.get('status', 'backlog'), data.get('priority', 'medium')))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"id": new_id}).encode())

    def do_PUT(self):
        if self.path.startswith('/api/tasks/'):
            task_id = self.path.split('/')[-1]
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (data['status'], task_id))
            conn.commit()
            conn.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

    def do_DELETE(self):
        if self.path.startswith('/api/tasks/'):
            task_id = self.path.split('/')[-1]
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "deleted"}')

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), UnifiedHandler) as httpd:
        print(f"ULTIMATE UNIFIED SERVER LIVE AT {PORT}")
        httpd.serve_forever()
