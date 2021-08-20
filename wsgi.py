import os
import sys
import json
import time
import locale

from runner import *
sys.path.insert(0, os.path.dirname(__file__))

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# server to host the program at invariants.1251.uk

def home_handler(environ, start_fn):
    start_fn('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    with open('index.html', 'r') as reader:
        return reader.read()

def invariant_handler(environ, start_fn):
    # start_fn('200 OK', [('Content-Type', 'text/json; charset=utf-8')])
    print(time.time())
    print(sys.version_info)
    print(sys.stdout.encoding)
    print(locale.getpreferredencoding())

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
    '/invariant': invariant_handler,
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
