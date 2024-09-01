import socketserver
import logging
import psutil

SERVER_HOST = '127.0.0.2'
SERVER_PORT = 8888

logging.basicConfig(level=logging.INFO)

class MainServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Main server received connection from: {self.client_address}")
        
        try:
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                logging.info("Main server received: {data.decode()}")
                response = "Echo from main server: " + data.decode()
                self.request.sendall(response.encode())
        
        except Exception as e:
            logging.error("An error occurred: {e}")
        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def monitor_server():
    logging.info("CPU usage: {psutil.cpu_percent()}%")
    logging.info("Memory usage: {psutil.virtual_memory().percent}%")

if __name__ == "__main__":
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), MainServerHandler)
    logging.info("Main server listening on {SERVER_HOST}:{SERVER_PORT}")
    
    # Monitor server stats
    monitor_server()
    
    server.serve_forever()
