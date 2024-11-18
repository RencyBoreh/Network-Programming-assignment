import socket
import threading
import os

# Directory to store uploaded files
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def handle_client(client_socket):
    try:
        # Receive the file name from the client
        file_name = client_socket.recv(1024).decode('utf-8')
        print(f"Receiving file: {file_name}")

        # Open a new file in the upload directory to write the incoming data
        with open(os.path.join(UPLOAD_DIR, file_name), 'wb') as f:
            while True:
                # Read 1024 bytes from the client
                data = client_socket.recv(1024)
                if not data:
                    break
                # Write the data to the file
                f.write(data)

        # Process the file (count the number of lines)
        file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(file_path, 'r') as f:
            line_count = sum(1 for line in f)
        
        # Send the result back to the client
        client_socket.send(f"File '{file_name}' has {line_count} lines.".encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the client connection
        client_socket.close()

def start_server():
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address and port
    server.bind(('0.0.0.0', 9999))
    # Listen for incoming connections (up to 5 simultaneous connections)
    server.listen(5)
    print("Server started on port 9999")

    while True:
        # Accept a new connection
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
