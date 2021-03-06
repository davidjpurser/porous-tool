#!/usr/bin/env python3

# Simple local server

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
from runner import *

import json
def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        print(parsed_path.path)
        if parsed_path.path == "/":

            with open('index.html', 'rb') as reader:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(reader.read())
                return
        else:
            try:
                with open(parsed_path.path[1:], 'rb') as reader:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(reader.read())
                    return
            except:
                self.send_response(404)

        return

    def do_POST(self):
        print('received a request')
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        if content_len > 0:
            data = json.loads(post_body)
        else: 
            data = {}

        output = service(data)

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'printed' : pyprint(output),
        }).encode())
        return

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8808), RequestHandler)
    print('Starting server at http://localhost:8808')
    server.serve_forever()