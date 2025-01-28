from socket import *

# Create the socket
s = socket(AF_INET, SOCK_STREAM)

# Bind to an address and port
s.bind(('localhost', 3303))  # Adjust the host and port as necessary

# Listen for incoming connections
s.listen(5)

print("Server is listening on port 3303...")

# Accept an incoming connection
(conn, addr) = s.accept()

print(f"Connection established with {addr}")

while True:
    # Receive data
    data = conn.recv(1024)
    if not data: 
        break
    msg = data.decode() + "*"
    
    # Send the modified message back
    conn.send(msg.encode())

# Close the connection
conn.close()

# Close the server socket
s.close()
