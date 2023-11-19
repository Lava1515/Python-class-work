from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

messages = []


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode())
        elif self.path == '/':
            with open('webroot/index.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/messages':
            content_length = int(self.headers['Content-Length'])
            content = self.rfile.read(content_length)
            message = json.loads(content.decode())
            messages.append({'content': message['content']})
            self.update_messages_file()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def update_messages_file(self):
        with open('messages.json', 'w') as file:
            json.dump(messages, file)


def main():
    global messages
    try:
        with open('messages.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError as e:
        # Create an empty messages.json file if not found
        with open('messages.json', 'w') as file:
            json.dump(messages, file)

    server_address = ('', 5000)
    httpd = HTTPServer(server_address, ChatHandler)
    print("Server is running on http://localhost:5000")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
