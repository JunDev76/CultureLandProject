import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

canStart = 0

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200, 'OK')
        self.send_header('Content-Type', 'text/plan')
        self.end_headers()
        global canStart
        if time.time() - canStart > 2:
            canStart = time.time()
            argv = self.path.split("/")
            del argv[0]
            os.system("start py cultureland.py " + "/".join(argv))


if __name__ == '__main__':
    server = HTTPServer(('', 15323), MyHandler)
    print('Started WebServer on port 15323...')
    print('Press ^c to quit webserver')
    server.serve_forever()

os.system("title CultureLandAPI - JunKR")
