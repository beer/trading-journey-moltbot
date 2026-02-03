import http.server
import socketserver
import json
import sqlite3
import os

PORT = 80
BASE_DIR = '/home/aliple/.openclaw/workspace/public'
DB_PATH = os.path.join(BASE_DIR, 'trading.db')

class SuperUnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('SELECT id, title, description, status, priority FROM tasks')
                tasks = [{"id": r[0], "title": r[1], "desc": r[2], "status": r[3], "priority": r[4]} for r in cursor.fetchall()]
                conn.close()
                self.wfile.write(json.dumps(tasks).encode())
            except Exception as e:
                self.wfile.write(json.dumps([]).encode())
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/tasks':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)',
                           (data['title'], data.get('desc', ''), data.get('status', 'backlog'), 'medium'))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps({"id": new_id}).encode())

    def do_PUT(self):
        if self.path.startswith('/api/tasks/'):
            task_id = self.path.split('/')[-1]
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET status = ?, title = ?, description = ? WHERE id = ?', 
                           (data.get('status'), data.get('title'), data.get('desc'), task_id))
            conn.commit()
            conn.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok": true}')

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SuperUnifiedHandler) as httpd:
        print(f"BATTLE-READY SERVER ON PORT {PORT}")
        httpd.serve_forever()
