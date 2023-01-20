from http.server import HTTPServer, BaseHTTPRequestHandler
from database import database
import json 

class HTTPMethods(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        name = json.loads(body.decode())['name']

        result = database.get_user(name)
        self.wfile.write(bytes(json.dumps(result), 'utf-8'))
 
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers() 
        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())['data']

        result = database.add_user(data)
        self.wfile.write(bytes(json.dumps(result), 'UTF-8'))

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        id = json.loads(body.decode())['id']

        result = database.delete_user(id)
        self.wfile.write(bytes(json.dumps(result), 'utf-8'))
    
    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        id = json.loads(body.decode())['id']
        data = json.loads(body.decode())['data']

        result = database.update_user(id, data)
        self.wfile.write(bytes(json.dumps(result), 'utf-8'))

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8000
    server = HTTPServer((HOST, PORT), HTTPMethods)
    print('Starting server on {}:{}'.format(HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print('Server Stopped')
