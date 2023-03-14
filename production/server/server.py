from database import database
import json

def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        params = environ['QUERY_STRING'].split('&')
        query_params = {}
        for param in params:
            key, value = param.split('=')
            query_params[key] = value

        if 'name' in query_params:
            name = query_params['name']
            result = database.get_user(name)
        elif 'date' in query_params:
            deadline = query_params['date']
            result = database.get_deadline(deadline)
        else:
            result = {'error': 'Please provide valid parameters'}
        
        response_body = json.dumps(result)
        status = '200 OK'
        headers = [('Content-type', 'application/json'), ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body.encode()]

    elif environ['REQUEST_METHOD'] == 'POST':
        params = environ['QUERY_STRING'].split('&')
        query_params = {}
        for param in params:
            key, value = param.split('=')
            query_params[key] = value

        if 'user' in query_params:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length)
            data = json.loads(body.decode())
            result = database.add_user(data)
        elif 'deadline' in query_params:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length)
            data = json.loads(body.decode())
            result = database.add_deadline(data)
        elif 'login' in query_params:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length)
            data = json.loads(body.decode())
            result = database.get_login_detail(data)
        else:
            result = {'error': 'Please provide valid parameters'}
        
        response_body = json.dumps(result)
        status = '200 OK'
        headers = [('Content-type', 'application/json'), ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body.encode()]

    elif environ['REQUEST_METHOD'] == 'DELETE':
        params = environ['QUERY_STRING'].split('&')
        query_params = {}
        for param in params:
            key, value = param.split('=')
            query_params[key] = value
            
        if '?' in environ['QUERY_STRING']:
            query_params = dict(q.split('=') for q in environ['QUERY_STRING'].split('&'))

        if 'user_id' in query_params:
            id = query_params['user_id']
            result = database.delete_user(id)
        elif 'task_id' in query_params:
            id = query_params['task_id']
            result = database.delete_deadline(id)
        else:
            result = {'error': 'Please provide valid parameters'}
        
        response_body = json.dumps(result)
        status = '200 OK'
        headers = [('Content-type', 'application/json'), ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body.encode()]

    elif environ['REQUEST_METHOD'] == 'PUT':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length)
        data = json.loads(body.decode())

        result = database.update_user(data)
        response_body = json.dumps(result)
        status = '200 OK'
        headers = [('Content-type', 'application/json'), ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body.encode()]

    else:
        status = '400 Bad Request'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return [b'Invalid request method']