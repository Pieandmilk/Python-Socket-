from socket import *
import threading
import os
import time

# Define host and port
HOST = "localhost"
PORT = 3303

# List to store chat history in chronological order: [[sender, message], ...]
chat_history = []

def clear_screen():
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")

def display_interface():
    """Clears the console and displays the updated chat history."""
    clear_screen()
    print("\n===== Chat History =====")
    for entry in chat_history:
        sender, msg = entry
        print(f"{sender}: {msg}")
    print("========================")
    print("Input Message: ", end="", flush=True)

def handle_client(conn, addr):
    """Handles communication with a connected client."""
    client_name = f"Client-{addr[1]}"  # Assign a unique name based on port

    print(f"\n[+] Connection established with {addr}")
    time.sleep(1)
    display_interface()
    
    def receive_messages():
        """Continuously listens for messages from the client."""
        while True:
            try:
                client_msg = conn.recv(1024).decode()
                if not client_msg:
                    break  # Stop if client disconnects
                if client_msg.lower() == "exit":
                    print(f"\n[-] {client_name} has disconnected.")
                    break

                chat_history.append([client_name, client_msg])  # Append to chronological history
                display_interface()  # Update UI

            except:
                break

    # Start receiving messages in a separate thread
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

    while True:
        server_msg = input().strip()

        if server_msg == "":
            continue  # Ignore empty messages

        chat_history.append(["Server", server_msg])  # Append to chronological history
        conn.send(server_msg.encode())  # Send message to client
        display_interface()  # Update UI after sending

        if server_msg.lower() == "exit":
            print("\n[-] Server is shutting down.")
            conn.close()
            break  # Exit only when the server chooses to shut down

def start_server():
    """Creates the server socket and listens for connections."""
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"\n[+] Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

def main():
    """Main function to start the server."""
    start_server()

if __name__ == "__main__":
    main()
