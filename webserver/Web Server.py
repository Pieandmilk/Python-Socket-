import socket

def start_server(host='127.0.0.1', port=80):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running at http://{host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")
        
        response = """HTTP/1.1 200 OK
        Content-Type: text/html; charset=UTF-8
        Connection: close
        Server: SimplePythonServer

        <html>
        <head><title>Simple Server</title></head>
        <body>
        <h1>Hello, World!</h1>
        
        </body>
        </html>
        """
        
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()
