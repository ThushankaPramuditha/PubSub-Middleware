import socket
import threading
import sys

clients = []
subscriptions = {}

def handle_client(client_socket, address):
    global subscriptions

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received message from {address}: {message}")
                
                parts = message.split(' ', 2)
                if len(parts) < 2:
                    continue
                
                role = parts[0].upper()
                topic = parts[1]
                
                if role == 'PUBLISHER':
                    if len(parts) < 3:
                        continue
                    msg = parts[2]
                    if msg.lower() == 'terminate':
                        print("Termination command received. Shutting down the server.")
                        client_socket.send("Server is shutting down.".encode())
                        for c in clients:
                            c.close()
                        server.close()
                        sys.exit(0)
                    if topic in subscriptions:
                        for subscriber in subscriptions[topic]:
                            try:
                                subscriber.send(f"{address} says: {msg}".encode())
                            except:
                                subscriptions[topic].remove(subscriber)
                elif role == 'SUBSCRIBER':
                    if topic not in subscriptions:
                        subscriptions[topic] = []
                    subscriptions[topic].append(client_socket)
            else:
                break
    except Exception as e:
        print(f"An error occurred with {address}: {e}")
    finally:
        client_socket.close()
        for topic, subs in subscriptions.items():
            if client_socket in subs:
                subs.remove(client_socket)
        print(f"Connection with {address} closed.")

def start_server(server_ip, server_port):
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <SERVER_PORT>")
        sys.exit(1)
    
    server_port = int(sys.argv[1])
    start_server('0.0.0.0', server_port)
