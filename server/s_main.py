import json
import os
import socketserver
from http.server import SimpleHTTPRequestHandler, HTTPServer

def getPort():
    try:
        with open("port.json", 'r') as f:
            data = json.load(f)
        if 'port' in data:
            return data['port']
        else:
            print(f"Warning: 'port' key not found in port.json")
            return None
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error: Could not read or parse JSON file: {e}")
        return None

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"  # Serve index.html by default

        try:
            # Check if the requested file exists
            if os.path.exists(self.translate_path(self.path)):
                # Serve the file using the parent class's method
                super().do_GET()
            else:
                # Send a 404 Not Found response if the file doesn't exist
                self.send_error(404, "File Not Found: %s" % self.path)
        except FileNotFoundError:
            self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"Received POST data: {post_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))

with socketserver.TCPServer(("", getPort()), MyHandler) as httpd:
  print("Serving at port", getPort())
  httpd.serve_forever()