from http.server import HTTPServer, BaseHTTPRequestHandler
from database import database, upload_avatar
import json 

class HTTPHandler(BaseHTTPRequestHandler):
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
            if 'uid' in query_params:
                uid = query_params['uid']
                deadline = query_params['date']
                result = database.get_deadline_for_user(uid, deadline)
            else:
                deadline = query_params['date']
                result = database.get_deadline(deadline)
        else:
            result = {'error': 'Please provide valid parameters'}
            
        self.wfile.write(bytes(json.dumps(result), 'UTF-8'))
 
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers() 
        
        query_params = {}
        if '?' in self.path:
            query_params = dict(q.split('=') for q in self.path.split('?')[1].split('&'))

        if 'avatar' in query_params:
            content_length = int(self.headers['Content-Length'])
            content_type = self.headers['Content-Type']
        if content_type == 'image/png' or content_type == 'image/jpeg':
            file_data = self.rfile.read(content_length)
            filename = 'image.jpg' if content_type == 'image/jpeg' else 'image.png'
            
            with open(filename, 'wb') as f:
                f.write(file_data)
            result = upload_avatar(filename)

        elif 'user' in query_params:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            result = database.add_user(data)
        elif 'deadline' in query_params:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            result = database.add_deadline(data)
        elif 'login' in query_params:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            result = database.get_login_detail(data)
        else:
            result = {'error': 'Please provide valid parameters'}
        
        self.wfile.write(bytes(json.dumps(result), 'UTF-8'))

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        query_params = {}
        if '?' in self.path:
            query_params = dict(q.split('=') for q in self.path.split('?')[1].split('&'))

        if 'user_id' in query_params:
            id = query_params['user_id']
            result = database.delete_user(id)
        elif 'task_id' in query_params:
            id = query_params['task_id']
            result = database.delete_deadline(id)
        else:
            result = {'error': 'Please provide valid parameters'}

        self.wfile.write(bytes(json.dumps(result), 'UTF-8'))
    
    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        query_params = {}
        if '?' in self.path:
            query_params = dict(q.split('=') for q in self.path.split('?')[1].split('&'))

        if 'task' in query_params:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            result = database.update_deadline(data)
        elif 'user' in query_params:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            result = database.update_user(data)
        else:
            result = {'error': 'Please provide valid parameters'}

        self.wfile.write(bytes(json.dumps(result), 'UTF-8'))


if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000
    server = HTTPServer((HOST, PORT), HTTPHandler)
    print(f'Starting server on {HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print('Server Stopped')
