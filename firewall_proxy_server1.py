import SocketServer
import socket
import threading
import time
from collections import defaultdict
import logging

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9999
MAIN_SERVER_HOST = '127.0.0.2'
MAIN_SERVER_PORT = 8888

# Rate limiting settings
RATE_LIMIT = 5  # Requests per second
RATE_LIMIT_WINDOW = 1  # Second

# Track request times
request_times = defaultdict(list)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        client_ip = self.client_address[0]
        current_time = time.time()
        
        # Clean up old requests
        request_times[client_ip] = [t for t in request_times[client_ip] if current_time - t < RATE_LIMIT_WINDOW]
        
        if len(request_times[client_ip]) >= RATE_LIMIT:
            logging.warning("Rate limit exceeded for %s", client_ip)
            self.request.sendall("Rate limit exceeded. Please try again later.")
            self.request.close()
            return
        
        request_times[client_ip].append(current_time)
        
        logging.info("Proxy server received connection from: %s", self.client_address)
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_server_socket:
                main_server_socket.connect((MAIN_SERVER_HOST, MAIN_SERVER_PORT))
                
                while True:
                    data = self.request.recv(1024)
                    if not data:
                        break
                    logging.info("Proxy server received: %s", data)
                    main_server_socket.sendall(data)
                    response = main_server_socket.recv(1024)
                    logging.info("Proxy server forwarding response: %s", response)
                    self.request.sendall(response)
        
        except Exception as e:
            logging.error("An error occurred: %s", e)
        finally:
            self.request.close()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def main():
    server = ThreadedTCPServer((PROXY_HOST, PROXY_PORT), ProxyServerHandler)
    logging.info("Proxy server listening on %s:%d", PROXY_HOST, PROXY_PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()
