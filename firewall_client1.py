import socket
import ssl
import time
import signal
import sys

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9999
MAX_RETRIES = 5

def signal_handler(sig, frame):
    print('Exiting client...')
    if 'client_socket' in globals():
        client_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    retries = 0
    while retries < MAX_RETRIES:
        try:
            context = ssl.create_default_context()
            client_socket = context.wrap_socket(client_socket, server_hostname=PROXY_HOST)
            client_socket.connect((PROXY_HOST, PROXY_PORT))
            break
        except socket.error as e:
            print("Connection failed ({retries + 1}/{MAX_RETRIES}): {e}")
            retries += 1
            time.sleep(2)
    else:
        print("Failed to connect after several retries.")
        return

    try:
        message = "Hello, Main Server via Proxy!"
        print("Client sending:", message)
        client_socket.sendall(message.encode())

        response = client_socket.recv(1024)
        print("Client received:", response.decode())

    except socket.error as e:
        print("Socket error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()
