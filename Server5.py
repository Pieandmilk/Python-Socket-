import socket
import threading
import tkinter as tk
from tkinter import ttk

# Server Config
HOST = "localhost"
PORT = 3303
clients = {}  # Dictionary to store client sockets and names
chat_history = []  # Stores messages

# GUI Setup
def setup_gui():
    global root, client_listbox, chat_text
    
    root = tk.Tk()
    root.title("Chat Server")
    root.geometry("500x400")
    
    notebook = ttk.Notebook(root)
    
    # Clients Tab
    client_frame = ttk.Frame(notebook)
    client_listbox = tk.Listbox(client_frame, width=50, height=20)
    client_listbox.pack(padx=10, pady=10)
    notebook.add(client_frame, text="Connected Clients")
    
    # Chat History Tab
    chat_frame = ttk.Frame(notebook)
    chat_text = tk.Text(chat_frame, width=60, height=20, state=tk.DISABLED)
    chat_text.pack(padx=10, pady=10)
    notebook.add(chat_frame, text="Chat History")
    
    notebook.pack(expand=True, fill="both")
    
    threading.Thread(target=start_server, daemon=True).start()
    root.mainloop()

# Update GUI
def update_chat():
    chat_text.config(state=tk.NORMAL)
    chat_text.delete(1.0, tk.END)
    for msg in chat_history:
        chat_text.insert(tk.END, msg + "\n")
    chat_text.config(state=tk.DISABLED)

def update_clients():
    client_listbox.delete(0, tk.END)
    for name in clients.keys():
        client_listbox.insert(tk.END, name)

# Broadcast Message
def broadcast(message, sender_conn=None):
    chat_history.append(message)
    update_chat()
    
    for client in clients.values():
        try:
            client['conn'].send(message.encode())
        except:
            remove_client(client['conn'])

# Send Chat History to New Clients
def send_chat_history(client_conn):
    if chat_history:
        history = "\n".join(chat_history)
        try:
            client_conn.send(history.encode())
        except:
            remove_client(client_conn)

# Handle Private Message
def handle_private_message(message, sender_conn, sender_name):
    parts = message.split(" ", 2)  # Format: /private <name> <message>
    if len(parts) < 3:
        return "Invalid private message format. Usage: /private <name> <message>"
    
    recipient_name = parts[1]
    private_msg = parts[2]
    
    # Find the recipient connection based on name
    recipient_conn = None
    for name, client in clients.items():
        if name == recipient_name:
            recipient_conn = client['conn']
            break
    
    if recipient_conn:
        recipient_conn.send(f"Private message from {sender_name}: {private_msg}".encode())
        return f"Private message sent to {recipient_name}"
    else:
        return f"Client with name {recipient_name} not found."

# Handle Client Connection
def handle_client(conn, addr):
    # Ask for client name
    conn.send("Enter your name: ".encode())
    name = conn.recv(1024).decode().strip()
    
    if name in clients:
        conn.send("Name already taken. Try again.".encode())
        conn.close()
        return
    
    clients[name] = {'conn': conn, 'addr': addr}
    update_clients()
    
    # Send chat history when client joins
    send_chat_history(conn)
    
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            
            if msg.startswith("/private"):
                response = handle_private_message(msg, conn, name)
                conn.send(response.encode())  # Send confirmation or error back to the sender
            else:
                broadcast(f"{name}: {msg}", conn)
    except:
        pass
    
    remove_client(conn)

# Remove Client from List
def remove_client(client_conn):
    for name, client in list(clients.items()):
        if client['conn'] == client_conn:
            del clients[name]
            update_clients()
            broadcast(f"Client {name} disconnected.")
            client_conn.close()
            break

# Start Server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    setup_gui()
