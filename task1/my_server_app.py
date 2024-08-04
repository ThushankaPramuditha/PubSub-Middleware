import socket
import sys

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_address = ('', port)
    server_socket.bind(server_address)
    
    server_socket.listen(1)
    print(f'Server started on port {port}. Waiting for a connection...')
    
    while True:
        connection, client_address = server_socket.accept()
        try:
            print(f'Connection from {client_address}')
            
            while True:
                data = connection.recv(1024).decode()
                if data:
                    print(f'Received: {data}')
                    if data.strip().lower() == 'terminate':
                        print('Terminate command received. Closing connection.')
                        break
                else:
                    break
        finally:
            connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python my_server_app.py <PORT>')
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)
