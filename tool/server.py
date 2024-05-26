from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000
WEB_DIR = "visualize"


class CustomHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path[-5:] == ".html" or self.path[-4:] == ".css" or self.path[-3:] == ".js" or self.path == "/" or self.path[-4:] == ".ico":
            self.path = "/" + WEB_DIR + self.path
        return SimpleHTTPRequestHandler.do_GET(self)


def start_server():
    handler = CustomHttpRequestHandler
    with HTTPServer(("", PORT), handler) as httpd:
        http_addr = f"http://{httpd.server_address[0]}:{httpd.server_address[1]}"
        print(http_addr)
        httpd.serve_forever()
