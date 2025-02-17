import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Client settings
HOST = "localhost"
PORT = 3303
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_name = ""  # Variable to store the client's name

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

def send_private_message():
    """Send a private message to another client."""
    message = message_entry.get()
    if message.startswith("/private"):
        client_socket.send(message.encode())  # Send the private message to the server
        message_entry.delete(0, tk.END)
    else:
        send_message()  # Normal message

# Prompt for Client Name
def request_name():
    global client_name
    name = input_name_entry.get().strip()
    if name:  # Proceed only if the name is not empty
        client_socket.send(name.encode())  # Send name to server
        response = client_socket.recv(1024).decode()  # Wait for server response
        
        if "Name already taken" in response:
            input_name_label.config(text="Name already taken. Try another name:")
            input_name_entry.delete(0, tk.END)
        else:
            client_name = name  # Store the client's name
            name_label.config(text=f"Connected as: {client_name}")  # Update the label
            input_name_frame.pack_forget()  # Hide name input frame after successful connection
            chat_frame.pack(fill="both", expand=True)  # Show chat interface
            threading.Thread(target=receive_messages, daemon=True).start()  # Start receiving messages

# GUI Setup
root = tk.Tk()
root.title("Client")

# Name Input Frame
input_name_frame = tk.Frame(root)
input_name_frame.pack(pady=10)

input_name_label = tk.Label(input_name_frame, text="Enter your name:")
input_name_label.pack(side=tk.LEFT)
input_name_entry = tk.Entry(input_name_frame)
input_name_entry.pack(side=tk.LEFT)

name_button = tk.Button(input_name_frame, text="Connect", command=request_name)
name_button.pack(side=tk.LEFT)

# Chat Interface (hidden until connected)
chat_frame = tk.Frame(root)

# Label to display client name at the top
name_label = tk.Label(chat_frame, text="Connected as: ", font=("Helvetica", 12, "bold"))
name_label.pack(pady=5)

# Chat History
chat_text = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED)
chat_text.pack(expand=True, fill="both")

# Input & Send Button
input_frame = tk.Frame(chat_frame)
input_frame.pack(fill="x")
message_entry = tk.Entry(input_frame)
message_entry.pack(side=tk.LEFT, expand=True, fill="x")
send_button = tk.Button(input_frame, text="Send", command=send_private_message)
send_button.pack(side=tk.RIGHT)

# GUI Changes (Optional): Add a label to guide users on private message format
private_msg_label = tk.Label(chat_frame, text="To send a private message, use: /private <name> <message>")
private_msg_label.pack()

# Run the GUI
root.mainloop()
