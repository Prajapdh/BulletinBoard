import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import socket
import json

# Initialize client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8090

# Global variables
alias = None

# Function to handle receiving messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('{') and message.endswith('}'):
                handle_json_message(json.loads(message))
            else:
                append_message(message)
        except Exception as e:
            append_message(f"Error: {e}")
            client.close()
            break


# Function to process JSON-formatted messages
def handle_json_message(message):
    if 'subject' in message:
        append_message(f"Message ID {message['id']} ({message['post_date']}): {message['subject']}")
        append_message(f"  {message['content']}")
    else:
        append_message(json.dumps(message))


# Function to append messages to the chat box
def append_message(message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, message + "\n")
    chat_box.see(tk.END)
    chat_box.config(state=tk.DISABLED)


# Function to send commands or messages to the server
def send_command(command):
    try:
        client.send(command.encode('utf-8'))
    except Exception as e:
        append_message(f"Error: {e}")


# GUI Button Functions
def join_group():
    group_name = simpledialog.askstring("Join Group", "Enter the group name to join:")
    if group_name:
        send_command(f"%groupjoin {group_name}")


def leave_group():
    group_name = simpledialog.askstring("Leave Group", "Enter the group name to leave:")
    if group_name:
        send_command(f"%groupleave {group_name}")


def view_users():
    group_name = simpledialog.askstring("View Users", "Enter the group name to view users:")
    if group_name:
        send_command(f"%groupusers {group_name}")


def retrieve_message():
    group_name = simpledialog.askstring("Retrieve Message", "Enter the group name:")
    if group_name:
        message_id = simpledialog.askstring("Retrieve Message", "Enter the message ID:")
        if message_id:
            send_command(f"%groupmessage {group_name} {message_id}")


def list_groups():
    send_command("%groups")


def post_message():
    group_name = simpledialog.askstring("Post Message", "Enter the group name:")
    if group_name:
        subject = simpledialog.askstring("Post Message", "Enter the subject:")
        if subject:
            content = simpledialog.askstring("Post Message", "Enter the message content:")
            if content:
                send_command(f"%grouppost {group_name} {subject} {content}")


def exit_chat():
    send_command("%exit")
    client.close()
    root.destroy()


# Function to initialize the client connection
def initialize_connection():
    try:
        client.connect((host, port))
        client.send(alias.encode('utf-8'))
        threading.Thread(target=receive_messages, daemon=True).start()
        append_message(f"Connected as {alias}.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to server: {e}")
        root.destroy()


# GUI Setup
root = tk.Tk()
root.title("Chat Client")
root.geometry("500x400")

# Chat display
chat_box = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Join Group", command=join_group).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Leave Group", command=leave_group).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="View Users", command=view_users).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Retrieve Message", command=retrieve_message).grid(row=0, column=3, padx=5, pady=5)

tk.Button(button_frame, text="List Groups", command=list_groups).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Post Message", command=post_message).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Exit", command=exit_chat).grid(row=1, column=2, padx=5, pady=5)


# Alias prompt and server connection
def prompt_alias_and_connect():
    global alias
    alias = simpledialog.askstring("Alias", "Enter your alias:")
    if not alias:
        messagebox.showerror("Error", "Alias cannot be empty.")
        root.destroy()
    else:
        threading.Thread(target=initialize_connection, daemon=True).start()


# Start the alias prompt after the GUI is fully initialized
root.after(100, prompt_alias_and_connect)

# Start the GUI
root.mainloop()