from socket import *

# Define host and port (should match the server settings)
HOST = 'localhost'  # Replace with the server's IP address if needed
PORT = 3303        # This should match the server's listening port

# Create the socket
s = socket(AF_INET, SOCK_STREAM)

try:
    # Connect to the server
    s.connect((HOST, PORT))
    
    # Send a message
    msg = "Hello World"
    s.send(msg.encode())
    
    # Receive data from the server
    data = s.recv(1024)
    print("Received from server:", data.decode())

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the socket
    s.close()
