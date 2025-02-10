import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Client settings
HOST = "localhost"
PORT = 3303
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_messages():
    """Continuously listen for messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, message + "\n")
            chat_text.config(state=tk.DISABLED)
            chat_text.yview(tk.END)
        except:
            break

def send_message():
    """Send a message to the server."""
    message = message_entry.get()
    if message:
        client_socket.send(message.encode())
        message_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Client")

# Chat History
chat_text = scrolledtext.ScrolledText(root, state=tk.DISABLED)
chat_text.pack(expand=True, fill="both")

# Input & Send Button
input_frame = tk.Frame(root)
input_frame.pack(fill="x")
message_entry = tk.Entry(input_frame)
message_entry.pack(side=tk.LEFT, expand=True, fill="x")
send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

# Start receiving messages in a thread
threading.Thread(target=receive_messages, daemon=True).start()

# Run the GUI
root.mainloop()
