import socket
import sys

def start_client(server_ip, server_port, role, topic):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    try:
        if role == 'PUBLISHER':
            while True:
                message = input("Enter message to send to the server (type 'terminate' to end): ")
                client.send(f"{role} {topic} {message}".encode())
                if message.lower() == 'terminate':
                    break
        elif role == 'SUBSCRIBER':
            client.send(f"{role} {topic}".encode())
            while True:
                message = client.recv(1024).decode()
                if message:
                    print(f"Received message: {message}")
                else:
                    break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python my_client_app.py <SERVER_IP> <SERVER_PORT> <ROLE> <TOPIC>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4]

    start_client(server_ip, server_port, role, topic)
