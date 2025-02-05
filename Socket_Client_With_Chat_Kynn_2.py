from socket import *
import threading
import os
import time

# Define host and port
HOST = "localhost"
PORT = 3303

# List to store chat history in chronological order: [[sender, message], ...]
chat_history = []

s = socket(AF_INET, SOCK_STREAM)

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

def receive_message():
    """Continuously listens for messages from the server."""
    while True:
        try:
            server_msg = s.recv(1024).decode()
            if not server_msg:
                break
            if server_msg.lower() == "exit":
                print("\n[-] Server has disconnected.")
                s.close()
                break

            # Update chat history with server's message
            chat_history.append(["Server", server_msg])
            display_interface()  # Update UI to show the new message

        except:
            break

def send_message():
    """Handles sending messages to the server."""
    while True:
        msg = input().strip()

        if msg == "":
            continue  # Ignore empty inputs

        # Update chat history with client's message
        chat_history.append(["Client", msg])
        s.send(msg.encode())

        if msg.lower() == "exit":
            print("\n[-] Disconnected from server.")
            s.close()
            break

        display_interface()  # Update UI after sending

def start_client():
    """Handles client connection and communication."""
    try:
        s.connect((HOST, PORT))
        print("\n[+] Connected to server.")
        time.sleep(1)
        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=receive_message, daemon=True)
        receive_thread.start()
        display_interface()
        # Send messages
        send_message()

    except Exception as e:
        print("\n[!] Error occurred:", e)

    finally:
        s.close()

def main():
    """Main function to start the client."""
    start_client()

if __name__ == "__main__":
    main()
