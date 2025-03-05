import socket
import threading
import os
import mimetypes

# Server Configuration
HOST = '127.0.0.1'  
PORT = 80  

# Function to handle client requests
def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        if not request:
            return
        
        # Extract requested file (default to index.html)
        request_line = request.split("\n")[0]
        requested_file = request_line.split(" ")[1]
        
        if requested_file == "/":
            requested_file = "/index.html"  # Default to index.html

        # Remove leading slash and get the full path
        file_path = "." + requested_file

        # Check if the file exists
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                response_body = file.read()
            
            # Get MIME type of file
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = "application/octet-stream"

            response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(response_body)}\r\n\r\n"
        
        else:
            # If file not found, return 404 error
            response_body = b"<h1>404 Not Found</h1>"
            response_headers = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n".format(len(response_body))
        
        # Send response
        client_socket.sendall(response_headers.encode() + response_body)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

# Function to start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on http://{HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Run the server
if __name__ == "__main__":
    start_server()
