import os
import sys
import json


from runner import *
sys.path.insert(0, os.path.dirname(__file__))


# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python v' + sys.version.split()[0] + '\n'
#     response = '\n'.join([message, version])
#     return [response.encode()]

def home_handler(environ, start_fn):
    start_fn('200 OK', [('Content-Type', 'text/html')])
    with open('index.html', 'rb') as reader:
        return reader.read()

def about_handler(environ, start_fn):
    # start_fn('200 OK', [('Content-Type', 'text/json; charset=utf-8')])
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    if request_body_size > 0:
        data = json.loads(request_body)
    else: 
        data = {}

    output = service(data)
    output = json.dumps({
        'printed' : pyprint(output)
    }).encode()
    # output = {x:output[x] for x in output if is_jsonable(output[x])}
    start_fn('200 OK', [
        ('Content-Type', 'text/json; charset=utf-8'),
        ('Content-Length', str(len(output)))
    ])
    return [output]


routes = {
    '/': home_handler,
    '/about': about_handler,
}


class Application(object):
    def __init__(self, routes):
        self.routes = routes

    def not_found(self, environ, start_fn):
        start_fn('404 Not Found', [('Content-Type', 'text/plain')])
        return ['404 Not Found']

    def __call__(self, environ, start_fn):
        handler = self.routes.get(environ.get('PATH_INFO')) or self.not_found
        return handler(environ, start_fn)

   

application = Application(routes)
