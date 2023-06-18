from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import time

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_PUT(self):
        print(time.time())
        content_length = int(self.headers['Content-Length'])
        print(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Post body received')


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        print(len(post_body))
        print(f"{time.time()}")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Post body received')

httpd = HTTPServer(('0.0.0.0', 443), MyServer)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    keyfile="./privkey.pem",
    certfile='./cert.pem',
    server_side=True
)

httpd.serve_forever()