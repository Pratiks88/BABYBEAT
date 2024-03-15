import socket
import threading
import random
import numpy as np
import sys

# Global variables
group_clients = []
server_clients = []
master_key = None
user_identity_matrices = []


def update_master_key():
    """Function to update the master key using matrix chain multiplication."""
    global user_identity_matrices
    # Ensure the user identity matrix has dimensions of 2x2 with random values
    user_identity_matrix = [[random.randint(2, 10), random.randint(2, 10)],
                            [random.randint(2, 10), random.randint(2, 10)]]
    user_identity_matrices.append(user_identity_matrix)
    if len(user_identity_matrices) == 1:
        new_master_key = np.prod(user_identity_matrix)
        print("New master key generated:", new_master_key)
        return new_master_key
    dimensions = [matrix[0] for matrix in user_identity_matrices]
    dimensions.append(user_identity_matrix[1][1])  # Add the last dimension
    n = len(user_identity_matrices)
    m = [[0] * n for _ in range(n)]

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = sys.maxsize
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dimensions[i][0] * dimensions[k][1] * dimensions[j][1]
                if q < m[i][j]:
                    m[i][j] = q

    # Compute the master key using the optimal parenthesization
    new_master_key = m[0][n - 1]
    print("New master key generated:", new_master_key)

    return new_master_key

def receive_messages(client_socket):
    """Function to continuously receive messages from a client."""
    try:
        while True:
            message = client_socket.recv(4096).decode()
            print("\n" + message)
            if client_socket in group_clients:
                # Check if the client's master key matches the group's master key
                client_master_key = get_client_master_key(client_socket)
                if client_master_key == master_key:
                    print(f"Client_key and Group key Matched and master key is {master_key}")
                    broadcast_message(message, client_socket)
                else:
                    handle_server_message(message, client_socket)
            elif client_socket in server_clients:
                print(f"Client_key and Group key Didnt Match, master key is {master_key} and client key is 0")
                handle_server_message(message, client_socket)
            else:
                # Handle messages from clients not added to the group
                handle_server_message(message, client_socket)
    except Exception as e:
        print(f"Error receiving message from client: {e}")

def get_client_master_key(client_socket):
    """Function to get the master key of a client."""
    return master_key


def broadcast_message(message, sender_socket):
    """Function to broadcast a message to all clients in the group."""
    for client in group_clients:
        if client != sender_socket:  # Exclude the sender
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")


def handle_server_message(message, client_socket):
    """Function to handle messages from clients communicating only with the server."""
    # Here you can implement custom handling for messages from server clients
    pass


def handle_new_client(client_socket):
    """Function to handle communication with a new client."""
    global master_key

    # Ask whether to include the new client in the group
    response = input("Do you want to include this client in the group? (yes/no): ").lower()
    if response == 'yes':
        old_master_key = master_key
        group_clients.append(client_socket)
        print("Client added to the group.")
        # Update the master key
        master_key = update_master_key()
        print("Old master key:", old_master_key)
        print("New master key:", master_key)
    else:
        print("Client not added to the group. It can communicate only with the server.")
        server_clients.append(client_socket)
        # Send the master keys to the denied client
        denied_message = f"Denied! Your master key: {0}\nGroup master key: {master_key}. So now you can only communicate with server"
        client_socket.sendall(denied_message.encode())

    # Start a thread to receive messages from the new client
    threading.Thread(target=receive_messages, args=(client_socket,)).start()


def main():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print("Server is listening for incoming connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Handle communication with the new client
        threading.Thread(target=handle_new_client, args=(client_socket,)).start()


if __name__ == "__main__":
    main()


