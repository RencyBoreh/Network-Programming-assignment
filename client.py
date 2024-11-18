import socket

def send_file(file_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    try:
        # Send the file name
        file_name = file_path.split('/')[-1]
        client.send(file_name.encode('utf-8'))

        # Send the file data
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client.sendall(data)

        # Receive the result from the server
        result = client.recv(1024).decode('utf-8')
        print(f"Server response: {result}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    file_path = input("Enter the path to the file to upload: ")
    send_file(file_path)
