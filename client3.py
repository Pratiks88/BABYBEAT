import socket
import threading

def receive_messages(client_socket):
    """Function to continuously receive messages from the server."""
    try:
        while True:
            message = client_socket.recv(4096).decode()
            print("\n" + message)
    except Exception as e:
        print(f"Error receiving message from server: {e}")

def send_messages(client_socket):
    """Function to send messages to the server."""
    try:
        while True:
            message = input("Enter message: ")
            client_socket.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to server: {e}")

def main():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Start a thread to receive messages from the server
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Start a thread to send messages to the server
    threading.Thread(target=send_messages, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
