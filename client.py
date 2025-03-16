import socket

# Client IP and Port configuration

def start_client(code):
    HOST = f'192.168.0.{code}'  # Server's IP address (localhost)
    PORT = 6000
    try:        # Port the server is listening on# Start the client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))  # Connect to the server
            client_socket.sendall("give me".encode())
            data = client_socket.recv(1024)  # Receive the response from the server
            print(f"{data.decode()}")
            while True:
                message = input("Enter your message (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Closing the connection...")
                    break
                if message == 'show':
                    client_socket.sendall("I showed".encode())
                data = client_socket.recv(1024)  # Receive the response from the server
                print(f"Server response: {data.decode()}")
    except OSError as e:
        print(f"Error: {e}, probably the code is incorrect or you are not on the same network, try again")
        start_client(input("Enter your code: "))
        
    print("Connection terminated.")
