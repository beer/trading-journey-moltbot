import http.server
import socketserver
import json
import sqlite3
import os

PORT = 8080
BASE_DIR = '/home/aliple/.openclaw/workspace'
DB_PATH = '/home/aliple/.openclaw/workspace/trading.db'

class FinalUnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

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
                self.wfile.write(b'[]')
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/tasks':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
                           (data['title'], data.get('desc', ''), data.get('status', 'backlog')))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps({"id": new_id}).encode())

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FinalUnifiedHandler) as httpd:
        print(f"TERMINAL READY ON PORT {PORT}")
        httpd.serve_forever()
