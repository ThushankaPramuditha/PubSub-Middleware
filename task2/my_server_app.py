import socket
import threading

publishers = []
subscribers = []

server_running = True

def handle_client(client_socket, client_address, role):
    global publishers, subscribers, server_running

    if role == "PUBLISHER":
        publishers.append(client_socket)
        print(f"[{client_address}] Connected as PUBLISHER")
    elif role == "SUBSCRIBER":
        subscribers.append(client_socket)
        print(f"[{client_address}] Connected as SUBSCRIBER")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.strip().lower() == "terminate":
                print(f"Received 'terminate' from {client_address}. Shutting down server.")
                server_running = False
                break
            if role == "PUBLISHER":
                print(f"[{client_address}] PUBLISHER: {message}")
                for subscriber in subscribers:
                    subscriber.send(message.encode('utf-8'))
    except:
        pass
    finally:
        if role == "PUBLISHER":
            publishers.remove(client_socket)
        elif role == "SUBSCRIBER":
            subscribers.remove(client_socket)
        client_socket.close()


def start_server(server_ip, server_port):
    global server_running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    all_clients = []

    def accept_clients():
        while server_running:
            try:
                server.settimeout(1.0)  
                client_socket, client_address = server.accept()
                role = client_socket.recv(1024).decode('utf-8')
                all_clients.append(client_socket)
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, role))
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Exception: {e}")
                break

    try:
       
        accept_thread = threading.Thread(target=accept_clients)
        accept_thread.start()
        while server_running:
            pass

        print("Server is shutting down...")
    finally:
        for client in all_clients:
            client.close()
        server.close()
        print("Server has shut down.")

start_server('0.0.0.0', 5000)
