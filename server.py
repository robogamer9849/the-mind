import socket
import threading
import random
from finder import *



nums = []

def get_min() :
    min_num = 100
    for i in nums:
        if i + 1 < min_num:
            min_num = i
    return min_num


# Server IP and Port configuration
HOST = '0.0.0.0'  # Server IP (localhost)
PORT = 6000     # Port for client connections# Function to manage client connections

def handle_client(conn, addr, num):
    print(f"Connection established with {addr}.")
    nums.append(num)
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                nums.remove(num)
                break

            print(f"Received from {addr}: {data.decode()}")

            if data.decode() == 'give me':
                conn.sendall(f"yor number: {num}\n".encode())

            elif data.decode() == 'I showed':
                print(nums)
                if num in nums:
                    if num == get_min():
                        conn.sendall(f"you are right\n".encode())
                    else:
                        conn.sendall(f"you lose\n".encode())

        except ConnectionResetError:
            print(f"Client {addr} has disconnected.")
            nums.remove(num)
            break
    conn.close()
    print(f"Connection with {addr} closed.")

# Start the server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}...")
        print("connect code:", find_code())
        
        while True:
            conn, addr = server_socket.accept()  # Accept a client connection
            thread = threading.Thread(target=handle_client, args=(conn, addr, random.randint(1, 100)))
            thread.start()  # Start a new thread for each client
            print(f"Active connections: {threading.active_count() - 1}")