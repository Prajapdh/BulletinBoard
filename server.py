import threading
import socket
import json
from datetime import datetime

host = "127.0.0.1"
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
names = []

groups = {
    'public': {'id': 0, 'members': [], 'messages': [], 'message_id_counter': 1},
    'group1': {'id': 1, 'members': [], 'messages': [], 'message_id_counter': 1},
    'group2': {'id': 2, 'members': [], 'messages': [], 'message_id_counter': 1},
    'group3': {'id': 3, 'members': [], 'messages': [], 'message_id_counter': 1},
    'group4': {'id': 4, 'members': [], 'messages': [], 'message_id_counter': 1},
    'group5': {'id': 5, 'members': [], 'messages': [], 'message_id_counter': 1}
}

def broadcast(message, group_members):
    for client in group_members:
        if client in clients:
            client.send(message)

def handle_connect(client):
    client.send(json.dumps({"groups": list(groups.keys())}).encode('utf-8'))

def join_group(client, group_name):
    if group_name in groups:
        groups[group_name]['members'].append(client)
        client.send(f"SERVER: You have joined {group_name}.".encode('utf-8'))
        broadcast(f"{names[clients.index(client)]} has joined {group_name}.".encode('utf-8'), groups[group_name]['members'])
    else:
        client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

def leave_group(client, group_name):
    if group_name in groups and client in groups[group_name]['members']:
        groups[group_name]['members'].remove(client)
        broadcast(f"{names[clients.index(client)]} has left {group_name}.".encode('utf-8'), groups[group_name]['members'])
    else:
        client.send(f"SERVER: You are not in {group_name}.".encode('utf-8'))

def post_message(client, group_name, subject, content):
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

def list_group_users(client, group_name):
    if group_name in groups:
        user_list = [names[clients.index(member)] for member in groups[group_name]['members']]
        client.send(f"SERVER: Users in {group_name}:\n".encode('utf-8') + "\n".join(user_list).encode('utf-8'))
    else:
        client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

def retrieve_message(client, group_name, message_id):
    if group_name in groups:
        for message in groups[group_name]['messages']:
            if message['id'] == int(message_id):
                client.send(json.dumps(message).encode('utf-8'))
                return
        client.send(f"SERVER: Message ID {message_id} not found in {group_name}.".encode('utf-8'))
    else:
        client.send(f"SERVER: Group {group_name} does not exist.".encode('utf-8'))

def show_help(client):
    help_message = (
        "Available commands:\n"
        "%groups - List all available groups\n"
        "%groupjoin <group_name> - Join a specific group\n"
        "%groupleave <group_name> - Leave a specific group\n"
        "%grouppost <group_name> <subject> <message> - Post a message to a specific group\n"
        "%groupusers <group_name> - List users in a specific group\n"
        "%groupmessage <group_name> <message_id> - Retrieve a specific message\n"
        "%exit - Exit the chat\n"
    )
    client.send(help_message.encode('utf-8'))

def handle_client(client):
    try:
        alias = client.recv(1024).decode('utf-8')
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
                elif command == '%help':
                    show_help(client)
                elif command == '%exit':
                    break
                else:
                    client.send("Invalid command.".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {names[clients.index(client)]}: {e}")
    finally:
        leave_group(client, 'public')
        if client in clients:
            index = clients.index(client)
            names.pop(index)
            clients.remove(client)
            client.close()

def receive():
    print("Server is running and listening...")
    while True:
        client, address = server.accept()
        print(f"Connection established with {address}")
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
