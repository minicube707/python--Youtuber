from http.server import HTTPServer, BaseHTTPRequestHandler
import time

# Server configuration
HOST = "0.0.0.0"
PORT = 9999

# Custom HTTP request handler
class NeuralHTTP(BaseHTTPRequestHandler):

    # Handle GET requests
    def do_GET(self):

        # Send HTTP 200 OK response
        self.send_response(200) 

        # Set response headers
        self.send_header("Content-type", "text/html")
        self.end_headers()

         # Send HTML content
        self.wfile.write(bytes("<html><body><h1>HELLO WORLD!</h1></body></html>", "utf-8"))

    # Handle POST requests
    def do_POST(self):

        # Send HTTP 200 OK response
        self.send_response(200)

        # Set response headers for JSON
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Get current date and time
        date = time.strftime("%Y-%m-%d %H-%M:%S", time.localtime(time.time()))

        # Send JSON response with current time
        self.wfile.write(bytes('{"time": "' + date + '"}', "utf-8"))

# Create the HTTP server
server = HTTPServer((HOST, PORT), NeuralHTTP)

print("Serveur now running...")
server.serve_forever()
server.server_close()
print("Server stopped!")