import http.server
import socketserver
import json
import sqlite3
import os

PORT = 80
BASE_DIR = '/home/aliple/.openclaw/workspace/public'
DB_PATH = '/home/aliple/.openclaw/workspace/public/trading.db'

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
        if self.path == '/api/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('SELECT id, title, description, status, priority FROM tasks')
                # 確保 key 是 desc，對齊前端
                tasks = [{"id": r[0], "title": r[1], "desc": r[2], "status": r[3], "priority": r[4]} for r in cursor.fetchall()]
                conn.close()
                self.wfile.write(json.dumps(tasks).encode())
            except Exception as e:
                self.wfile.write(json.dumps([{"id":0, "title": "Error", "desc": str(e), "status":"backlog"}]).encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), UnifiedHandler) as httpd:
        httpd.serve_forever()
