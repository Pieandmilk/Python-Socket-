import socket
import os

def serve_file(file_path, content_type):
    """Reads and serves a file if it exists"""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nConnection: close\r\n\r\n"
        return response.encode() + data
    else:
        return b"HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\nFile Not Found"

def start_server(host='127.0.0.1', port=80):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running at http://{host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        request_lines = request.split("\n")
        if len(request_lines) > 0:
            request_path = request_lines[0].split(" ")[1]
        else:
            request_path = "/"

        if request_path == "/ratdance.mp4":
            response = serve_file("ratdance.mp4", "video/mp4")
        elif request_path == "/ratBG.jpg":
            response = serve_file("ratBG.jpg", "image/jpeg")
        else:
            response = """HTTP/1.1 200 OK
            Content-Type: text/html; charset=UTF-8\r\nConnection: close\r\n\r\n
            <html>
            <head>
            <title>Surprise Page</title>
            <style>
                body {
                    background-image: url('ratBG.jpg');
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                    text-align: center;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                #message-container {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    text-align: center;
                    background: rgba(0, 0, 0, 0.5);
                    padding: 20px;
                    border-radius: 10px;
                }
                h1 {
                    font-size: 36px;
                    margin-bottom: 10px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 20px;
                    background-color: red;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                #content {
                    display: none;
                    text-align: center;
                }
                video {
                    width: 830px;
                    height: 1108px;
                    display: block;
                    margin: auto;
                }
            </style>
            </head>
            <body>
            
            <div id="message-container">
                <h1>Do you want a surprise?</h1>
                <button onclick="showSurprise()">Surprise!</button>
            </div>

            <div id="content">
                <h1>YOU BEEN RATTED!</h1>
                <video id="ratVideo" autoplay loop>
                    <source src="ratdance.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>

            <script>
                function showSurprise() {
                    document.getElementById("message-container").style.display = "none";
                    document.getElementById("content").style.display = "block";
                    document.getElementById("ratVideo").play();
                }
            </script>

            </body>
            </html>
            """
            response = response.encode()

        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    start_server()
