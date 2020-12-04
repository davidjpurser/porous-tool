#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
from runner import service

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if self.path == "/index.html":
            with open('index.html', 'rb') as reader:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(reader.read())
                return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())
        return

    def do_POST(self):
        print('hello')
        content_len = int(self.headers.get('content-length'))
        print(content_len)
        post_body = self.rfile.read(content_len)
        print(post_body)
        if content_len > 0:
            data = json.loads(post_body)
        else: 
            data = {}
        print(data)

        again = service(data)


        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'output' : again,
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version,
            'body': data
        }).encode())
        return

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Starting server at http://localhost:8000')
    server.serve_forever()