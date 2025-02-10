import socket
import threading
import tkinter as tk
from tkinter import ttk

# Server Config
HOST = "localhost"
PORT = 3303
clients = {}  # Dictionary to store client sockets
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
    for addr in clients.values():
        client_listbox.insert(tk.END, str(addr))

# Broadcast Message
def broadcast(message, sender_conn=None):
    chat_history.append(message)
    update_chat()
    
    for client in clients.keys():
        try:
            client.send(message.encode())
        except:
            remove_client(client)

# Send Chat History to New Clients
def send_chat_history(client):
    if chat_history:
        history = "\n".join(chat_history)
        try:
            client.send(history.encode())
        except:
            remove_client(client)

# Handle Client Connection
def handle_client(conn, addr):
    clients[conn] = addr
    update_clients()
    
    # Send chat history when client joins
    send_chat_history(conn)
    
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            broadcast(f"{addr}: {msg}", conn)
    except:
        pass
    
    remove_client(conn)

# Remove Client from List
def remove_client(client):
    if client in clients:
        addr = clients[client]
        del clients[client]
        update_clients()
        broadcast(f"Client {addr} disconnected.")
        client.close()

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
