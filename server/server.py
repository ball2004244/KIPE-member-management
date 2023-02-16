from http.server import HTTPServer, BaseHTTPRequestHandler
from database import database
import json 
import urllib.parse as urlparse
from datetime import datetime

class HTTPMethods(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        query_params = {}
        if '?' in self.path:
            query_params = dict(q.split('=') for q in self.path.split('?')[1].split('&'))

        if 'name' in query_params:
            name = query_params['name']
            result = database.get_user(name)
        elif 'date' in query_params:
            raw_deadline = query_params['date']
            decoded_deadline = urlparse.unquote(raw_deadline)
            
            deadline = decoded_deadline.replace('+', ' ')
            result = database.get_deadline(deadline)
        else:
            result = {'error': 'Please provide either name or date parameter'}
            
        self.wfile.write(bytes(json.dumps(result, cls=CustomEncoder), 'utf-8'))
 
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers() 
        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())

        result = database.add_user(data)
        self.wfile.write(bytes(json.dumps(result), 'UTF-8'))

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        id = json.loads(body.decode())

        result = database.delete_user(id)
        self.wfile.write(bytes(json.dumps(result), 'utf-8'))
    
    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())
        print(data)
        result = database.update_user(data)
        self.wfile.write(bytes(json.dumps(result), 'utf-8'))

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000
    server = HTTPServer((HOST, PORT), HTTPMethods)
    print(f'Starting server on {HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print('Server Stopped')
