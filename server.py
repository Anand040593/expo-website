import http.server
import socketserver
import json
import sqlite3
import csv
from io import StringIO
import socket
import secrets
import hashlib

DB_NAME = 'expo.db'

# Simple in-memory session store for demo
SESSIONS = set()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Event registrations
    c.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            item_name TEXT,
            amount INTEGER
        )
    ''')
    
    # Stall bookings
    c.execute('''
        CREATE TABLE IF NOT EXISTS stall_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            company_name TEXT,
            company_desc TEXT,
            package_name TEXT,
            amount INTEGER
        )
    ''')
    
    # Admins table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Insert default admin with HASHED password if not exists
    c.execute("SELECT id FROM admins WHERE username='admin'")
    if not c.fetchone():
        hashed_pw = hash_password('admin')
        c.execute("INSERT INTO admins (username, password) VALUES ('admin', ?)", (hashed_pw,))
        
    conn.commit()
    conn.close()

class ExpoHandler(http.server.SimpleHTTPRequestHandler):
    def handle(self):
        try:
            super().handle()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError, socket.error):
            pass
            
    def check_auth(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return False
        
        cookies = dict(item.split("=") for item in cookie_header.split("; ") if "=" in item)
        session_id = cookies.get('session_id')
        
        return session_id in SESSIONS

    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = data.get('username')
            password = data.get('password')
            hashed_input_pw = hash_password(password)
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            # Check against hashed password in database
            c.execute("SELECT id FROM admins WHERE username=? AND password=?", (username, hashed_input_pw))
            row = c.fetchone()
            conn.close()
            
            if row:
                session_id = secrets.token_hex(16)
                SESSIONS.add(session_id)
                self.send_response(200)
                self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly; SameSite=Strict')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid credentials'}).encode('utf-8'))
                
        elif self.path == '/api/logout':
            self.send_response(200)
            self.send_header('Set-Cookie', 'session_id=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))

        elif self.path == '/api/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                
                if data.get('is_stall'):
                    c.execute('''
                        INSERT INTO stall_bookings (name, email, phone, address, company_name, company_desc, package_name, amount)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        data.get('name'), data.get('email'), data.get('phone'), data.get('address'),
                        data.get('company_name'), data.get('company_desc'), data.get('item_name'), data.get('amount')
                    ))
                else:
                    c.execute('''
                        INSERT INTO members (name, email, phone, address, item_name, amount)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        data.get('name'), data.get('email'), data.get('phone'), data.get('address'),
                        data.get('item_name'), data.get('amount')
                    ))
                    
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "File not found")

    def do_GET(self):
        # Protected API Routes
        if self.path in ['/api/members', '/api/stalls'] or self.path.startswith('/api/export'):
            if not self.check_auth():
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode('utf-8'))
                return

        if self.path == '/api/members':
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('SELECT timestamp, name, email, phone, address, item_name, amount FROM members ORDER BY id DESC')
            rows = c.fetchall()
            conn.close()
            
            result = []
            for row in rows:
                result.append({
                    'timestamp': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'address': row[4],
                    'item_name': row[5],
                    'amount': row[6]
                })
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        elif self.path == '/api/stalls':
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('SELECT timestamp, name, email, phone, address, company_name, company_desc, package_name, amount FROM stall_bookings ORDER BY id DESC')
            rows = c.fetchall()
            conn.close()
            
            result = []
            for row in rows:
                result.append({
                    'timestamp': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'address': row[4],
                    'company_name': row[5],
                    'company_desc': row[6],
                    'package_name': row[7],
                    'amount': row[8]
                })
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        elif self.path.startswith('/api/export'):
            # Check for type parameter e.g., /api/export?type=stalls
            is_stalls = '?type=stalls' in self.path
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            
            si = StringIO()
            cw = csv.writer(si)
            
            if is_stalls:
                c.execute('SELECT timestamp, name, email, phone, address, company_name, company_desc, package_name, amount FROM stall_bookings ORDER BY id DESC')
                rows = c.fetchall()
                cw.writerow(['Timestamp', 'Name', 'Email', 'Phone', 'Address', 'Company Name', 'Company Details', 'Package', 'Amount Paid (INR)'])
                cw.writerows(rows)
                filename = "stall_bookings.csv"
            else:
                c.execute('SELECT timestamp, name, email, phone, address, item_name, amount FROM members ORDER BY id DESC')
                rows = c.fetchall()
                cw.writerow(['Timestamp', 'Name', 'Email', 'Phone', 'Address', 'Item/Event', 'Amount Paid (INR)'])
                cw.writerows(rows)
                filename = "event_registrations.csv"
                
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-type', 'text/csv')
            self.end_headers()
            self.wfile.write(si.getvalue().encode('utf-8'))
            
        else:
            try:
                super().do_GET()
            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError, socket.error):
                pass

if __name__ == '__main__':
    init_db()
    PORT = 8000
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), ExpoHandler) as httpd:
        print(f"Serving concurrently at port {PORT}")
        httpd.serve_forever()
