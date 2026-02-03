import http.server
import socketserver
import json
import sqlite3
import os
from urllib.parse import urlparse, parse_qs

PORT = 80
DB_PATH = '/home/aliple/.openclaw/workspace/public/trading.db'
DIRECTORY = '/home/aliple/.openclaw/workspace/public'

class TradingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

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
            super().do_GET()

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
            self.wfile.write(json.dumps({"status": "success", "id": new_id}).encode())

    def do_DELETE(self):
        if self.path.startswith('/api/tasks'):
            task_id = self.path.split('/')[-1]
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "deleted"}')

    def do_PUT(self):
        if self.path.startswith('/api/tasks'):
            task_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = json.loads(self.rfile.read(content_length))
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            if 'status' in put_data:
                cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (put_data['status'], task_id))
            conn.commit()
            conn.close()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "updated"}')

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), TradingHandler) as httpd:
        print(f"Aliple Native Server running on Port {PORT}")
        httpd.serve_forever()
