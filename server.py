import threading
import socket
import json
from datetime import datetime

# Server configuration
host = "127.0.0.1"  # Localhost
port = 8080  # Port number
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket for TCP
server.bind((host, port))  # Bind the server to the address and port
server.listen()  # Start listening for incoming connections

# Lists to manage connected clients and their aliases
clients = []
names = []

# Dictionary to manage groups, their members, and messages
groups = {
    'public': {'id': 0, 'members': [], 'messages': [], 'message_id_counter': 1},
    'Study': {'id': 1, 'members': [], 'messages': [], 'message_id_counter': 1},
    'Movies': {'id': 2, 'members': [], 'messages': [], 'message_id_counter': 1},
    'Music': {'id': 3, 'members': [], 'messages': [], 'message_id_counter': 1},
    'Career': {'id': 4, 'members': [], 'messages': [], 'message_id_counter': 1},
    'Announcements': {'id': 5, 'members': [], 'messages': [], 'message_id_counter': 1},
}

def broadcast(message, group_members, exclude_client=None):
    """
    Sends a message to all members of a group, excluding a specified client (if any).
    """
    for client in group_members:
        if client in clients and client != exclude_client:
            client.send(message)

def handle_connect(client):
    """
    Sends the list of available groups to the client upon connection.
    """
    client.send(json.dumps({"groups": list(groups.keys())}).encode('utf-8'))

def join_public(client):
    """
    Adds a client to the public group.
    """
    join_group(client, 'public')

def post_public(client, subject, content):
    """
    Posts a message to the public group.
    """
    post_message(client, 'public', subject, content)

def list_public_users(client):
    """
    Lists all users in the public group.
    """
    list_group_users(client, 'public')

def leave_public(client):
    """
    Removes a client from the public group.
    """
    leave_group(client, 'public')

def retrieve_public_message(client, message_id):
    """
    Retrieves a specific message from the public group.
    """
    retrieve_message(client, 'public', message_id)

# def join_group(client, group_name):
#     if group_name in groups:
#         groups[group_name]['members'].append(client)
#         client.send(f"SERVER: You have joined {group_name}.".encode('utf-8'))
#         broadcast(f"{names[clients.index(client)]} has joined {group_name}.".encode('utf-8'), groups[group_name]['members'])
#     else:
#         client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

#     """
#     Adds a client to a group and notifies the group members.
#     """

def join_group(client, group_name):
    """
    Adds a client to a group and sends relevant notifications/messages.
    """
    if group_name in groups:
        # Check if the client is already in the group
        if client in groups[group_name]['members']:
            client.send(f"SERVER: You are already a member of {group_name}.".encode('utf-8'))
            return

        # Add the client to the group
        groups[group_name]['members'].append(client)

        # Notify all members of the group
        broadcast(f"{names[clients.index(client)]} has joined {group_name}.\n".encode('utf-8'), groups[group_name]['members'])

        # Send confirmation to the new user
        client.send(f"SERVER: You have joined {group_name}.\n".encode('utf-8'))

        # Send the list of all group members to the new user
        user_list = [names[clients.index(member)] for member in groups[group_name]['members']]
        client.send(f"SERVER: Members of {group_name}: {', '.join(user_list)}\n".encode('utf-8'))

        # Send the last two messages of the group to the new user
        last_messages = groups[group_name]['messages'][-2:]
        if last_messages:
            for message in last_messages:
                client.send(f"SERVER: Last message from {message['sender']} ({message['post_date']}): {message['subject']} - {message['content']}\n".encode('utf-8'))
    else:
        # Notify the user if the group does not exist
        client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

def list_group_users(client, group_name):
    """
    Lists all users in a specific group.
    """
    if group_name in groups:
        user_list = [names[clients.index(member)] for member in groups[group_name]['members']]
        client.send(f"SERVER: Users in {group_name}:\n".encode('utf-8') + "\n".join(user_list).encode('utf-8'))
    else:
        client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

def post_message(client, group_name, subject, content):
    """
    Posts a message to a group and broadcasts it to the group members.
    """
    if group_name in groups and client in groups[group_name]['members']:
        message_id = groups[group_name]['message_id_counter']
        message = {
            'id': message_id,
            'sender': names[clients.index(client)],
            'post_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'subject': subject,
            'content': content
        }
        groups[group_name]['messages'].append(message)
        groups[group_name]['message_id_counter'] += 1
        broadcast(json.dumps(message).encode('utf-8'), groups[group_name]['members'])
    else:
        client.send(f"SERVER: You are not a member of {group_name}.".encode('utf-8'))

def retrieve_message(client, group_name, message_id):
    """
    Retrieves a specific message from a group by message ID.
    """
    if group_name in groups:
        for message in groups[group_name]['messages']:
            if message['id'] == int(message_id):
                client.send(json.dumps(message).encode('utf-8'))
                return
        client.send(f"SERVER: Message ID {message_id} not found in {group_name}.".encode('utf-8'))
    else:
        client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

# def leave_group(client, group_name):
#     """
#     Removes a client from a group and notifies the group members.
#     """
#     if group_name in groups and client in groups[group_name]['members']:
#         groups[group_name]['members'].remove(client)
#         broadcast(f"{names[clients.index(client)]} has left {group_name}.".encode('utf-8'), groups[group_name]['members'])
#     else:
#         client.send(f"SERVER: You are not in {group_name}.".encode('utf-8'))

def leave_group(client, group_name):
    """
    Removes a client from a group and notifies the group members.
    """
    if group_name in groups and client in groups[group_name]['members']:
        groups[group_name]['members'].remove(client)
        broadcast(f"{names[clients.index(client)]} has left {group_name}.".encode('utf-8'), groups[group_name]['members'])
        client.send(f"SERVER: You have left {group_name}.".encode('utf-8'))
    else:
        client.send(f"SERVER: You are not in {group_name}.".encode('utf-8'))

def show_help(client):
    """
    Sends the list of available commands to the client.
    """
    help_message = (
        "Available commands:\n"
        "%groups - List all available groups\n"
        "%groupjoin <group_name> - Join a specific group\n"
        "%groupleave <group_name> - Leave a specific group\n"
        "%grouppost <group_name> <subject> <message> - Post a message to a specific group\n"
        "%groupusers <group_name> - List users in a specific group\n"
        "%groupmessage <group_name> <message_id> - Retrieve a specific message\n"
        "%join - Join the public group\n"
        "%post <subject> <message> - Post a message to the public group\n"
        "%users - List users in the public group\n"
        "%leave - Leave the public group\n"
        "%message <message_id> - Retrieve a specific message from the public group\n"
        "%exit - Exit the chat\n"
        "%help - Show this help message\n"
    )
    client.send(help_message.encode('utf-8'))

def handle_client(client):
    """
    Handles interaction with an individual client.
    """
    try:
        alias = client.recv(1024).decode('utf-8')  # Receive alias from client
        names.append(alias)
        clients.append(client)
        client.send(f"Welcome {alias}!\n".encode('utf-8'))
        join_group(client, 'public')

        while True:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('%'):
                command, *args = message.split()
                if command == '%groups':
                    handle_connect(client)
                elif command == '%groupjoin' and len(args) == 1:
                    join_group(client, args[0])
                elif command == '%groupleave' and len(args) == 1:
                    leave_group(client, args[0])
                elif command == '%grouppost' and len(args) >= 3:
                    post_message(client, args[0], args[1], ' '.join(args[2:]))
                elif command == '%groupusers' and len(args) == 1:
                    list_group_users(client, args[0])
                elif command == '%groupmessage' and len(args) == 2:
                    retrieve_message(client, args[0], args[1])
                elif command == '%join':
                    join_public(client)
                elif command == '%post' and len(args) >= 2:
                    post_public(client, args[0], ' '.join(args[1:]))
                elif command == '%users':
                    list_public_users(client)
                elif command == '%leave':
                    leave_public(client)
                elif command == '%message' and len(args) == 1:
                    retrieve_public_message(client, args[0])
                elif command == '%help':
                    show_help(client)
                elif command == '%exit':
                    break
                else:
                    client.send("Invalid command.".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {names[clients.index(client)]}: {e}")
    finally:
        leave_group(client, 'public')  # Remove client from public group
        if client in clients:
            index = clients.index(client)
            names.pop(index)
            clients.remove(client)
            client.close()

def receive():
    """
    Listens for and accepts new client connections.
    """
    print("Server is running and listening...")
    while True:
        client, address = server.accept()
        print(f"Connection established with {address}")
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()