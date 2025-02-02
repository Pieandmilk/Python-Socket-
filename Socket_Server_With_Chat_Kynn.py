from socket import *

# Define host and port
HOST = "192.168.56.1"
PORT = 3303

# Create the socket
s = socket(AF_INET, SOCK_STREAM)

# Bind to the address and port
s.bind((HOST, PORT))

# Listen for incoming connections
s.listen(1)
print("Server is listening on port 3303...")

# Accept an incoming connection
conn, addr = s.accept()
print(f"Connection established with {addr}")

while True:
    # Receive message from client
    client_msg = conn.recv(1024).decode()
    
    # Check if client wants to exit
    if client_msg.lower() == "exit":
        print("Client has disconnected.")
        break
    
    print(f"Client: {client_msg}")
    
    # Get server response
    server_msg = input("Server: ")
    
    # Send response to client
    conn.send(server_msg.encode())

    # Check if server wants to exit
    if server_msg.lower() == "exit":
        print("Server is shutting down.")
        break

# Close connection
conn.close()
s.close()
