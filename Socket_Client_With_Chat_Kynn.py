from socket import *

# Define host and port
HOST = "192.168.56.1"
PORT = 3303

# Create the socket
s = socket(AF_INET, SOCK_STREAM)

try:
    # Connect to the server
    s.connect((HOST, PORT))
    
    while True:
        # Get user input
        msg = input("Client: ")
        
        # Send message to server
        s.send(msg.encode())
        
        # Check if client wants to exit
        if msg.lower() == "exit":
            print("Disconnected from server.")
            break

        # Receive response from server
        server_msg = s.recv(1024).decode()
        
        # Check if server wants to exit
        if server_msg.lower() == "exit":
            print("Server has disconnected.")
            break
        
        print(f"Server: {server_msg}")

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the socket
    s.close()
