import socket
import sys

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)
    
    try:
        while True:
            message = input("Enter message to send to the server (type 'terminate' to quit): ")
            client_socket.sendall(message.encode())
            if message.strip().lower() == 'terminate':
                print('Terminate command sent. Closing connection.')
                break
    finally:
        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python my_client_app.py <SERVER_IP> <SERVER_PORT>')
        sys.exit(1)
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    start_client(server_ip, server_port)
