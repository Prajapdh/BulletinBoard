## *Project Overview*
This project includes two main components:
1. *Server (server.py)*: Manages group chats, handles client connections, and broadcasts messages.
2. *Client (client.py)*: Allows users to connect to the server, join groups, send messages, and interact with group members.

The programs are written in Python and use sockets for communication.

---

## *Setup Instructions*
### *Prerequisites*
1. *Python Installation*:
   - Ensure Python 3.x is installed on your machine.
   - Verify installation:
     bash
     python --version
     
   - Install missing dependencies if needed:
     bash
     pip install --upgrade pip
     

2. *JSON (Native to Python)*:
   The json library is included by default in Python 3.x, so no additional installation is required.

---

## *Compilation and Execution*

### *Running the Server*
1. Open a terminal.
2. Navigate to the directory containing server.py.
3. Run the server:
   bash
   python server.py
   
4. The server will start listening for client connections on 127.0.0.1 at port 8080.

---

### *Running the Client*
1. Open a new terminal for each client.
2. Navigate to the directory containing client.py.
3. Run the client:
   bash
   python client.py
   
4. When prompted, enter an alias (e.g., John) to identify yourself in the chat.
5. Use the available commands (see below) to interact with the server and other users.

---

## *Usability Instructions*
### *Available Commands*
These commands can be typed into the client terminal to interact with the server:
- *%groups*: List all available groups on the server.
- *%groupjoin <group_name>*: Join a specific group. Example:
  
  %groupjoin public
  
- *%groupleave <group_name>*: Leave the current group. Example:
  
  %groupleave public
  
- *%grouppost <group_name> <subject> <message>*: Post a message to a group. Example:
  
  %grouppost public "Meeting" "Let’s discuss the agenda."
  
- *%groupusers <group_name>*: List all users in a specific group.
- *%groupmessage <group_name> <message_id>*: Retrieve a specific message by ID from a group.
- *%help*: Display a list of available commands and their usage.
- *%exit*: Disconnect from the server and exit.

---

## *Error Handling and Known Issues*

### *Major Issues Encountered*
1. *Concurrent Access to Resources*:
   - *Issue*: Race conditions could occur when multiple clients access or modify shared data (e.g., group membership).
   - *Solution*: Used Python’s threading module to handle multiple client connections safely.

2. *Client Disconnections*:
   - *Issue*: When a client disconnected abruptly, the server threw an error.
   - *Solution*: Added error handling to gracefully remove disconnected clients.

3. *JSON Parsing*:
   - *Issue*: Messages were being improperly formatted as JSON strings.
   - *Solution*: Implemented strict formatting for message serialization and deserialization using Python's json library.

4. *Message Retrieval*:
   - *Issue*: Users outside a group could attempt to retrieve messages.
   - *Solution*: Added validation to ensure users can only retrieve messages from groups they have joined.

### *Unresolved Issues*
- Currently, no significant unresolved issues.

---

## *Comments*
### *Server (server.py)*
- The server creates a socket that listens on 127.0.0.1:8080.
- Manages clients using the threading module.
- Handles:
  - Broadcasting messages to group members.
  - Maintaining group memberships and messages.
  - Providing help and feedback to users.

### *Client (client.py)*
- The client connects to the server and provides an interface to interact with groups.
- Features:
  - Support for multiple commands.
  - Ability to join/leave groups and retrieve messages.
  - Graceful disconnection handling.

---

## *Example Usage*

### *Scenario: John and Alice Join and Chat in public*
1. *Start the server*:
   bash
   python server.py
   
   Output:
   
   Server is running and listening...
   

2. *Start John’s client*:
   bash
   python client.py
   
   Input:
   
   Choose an alias >>> John
   
   Commands:
   
   %groupjoin public
   %grouppost public "Hello" "Hi everyone!"
   

3. *Start Alice’s client*:
   bash
   python client.py
   
   Input:
   
   Choose an alias >>> Alice
   
   Commands:
   
   %groupjoin public
   

4. *John and Alice See Each Other’s Messages*:
   Both clients will display:
   
   SERVER: You have joined public.
   John: Hi everyone!