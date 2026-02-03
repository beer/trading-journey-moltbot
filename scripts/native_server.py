import http.server
import socketserver
import json
import sqlite3
import os

PORT = 8080
BASE_DIR = '/home/aliple/.openclaw/workspace/public'
DB_PATH = '/home/aliple/.openclaw/workspace/public/trading.db'

class TradingHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 這是解決瀏覽器攔截的關鍵：加入 CORS 頭
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # 預檢請求
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
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
            os.chdir(BASE_DIR)
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)',
                           (post_data['title'], post_data.get('description', ''), post_data.get('status', 'backlog'), post_data.get('priority', 'medium')))
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
            content_length = int(self.headers['Content-Length'])
            put_data = json.loads(self.rfile.read(content_length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (put_data['status'], task_id))
            conn.commit()
            conn.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "updated"}')

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
    with socketserver.TCPServer(("", PORT), TradingHandler) as httpd:
        print(f"Server is LIVE at Port {PORT}")
        httpd.serve_forever()
