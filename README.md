## Bulletin Board Using Socket Programming
### Team Members:
- Daksh Prajapati
- Varad Parte
- Arya Narke

This project includes:
1. **Server (server.py): Manages group chats, client connections, and broadcasts messages.
2. **Client (client.py): Allows users to connect to the server, join groups, send messages, and interact with group members.

The programs are written in Python and use sockets for communication.

---

## *Setup Instructions*

### *Prerequisites*
1. Install Python (version 3.x or above):
   - [Python Download](https://www.python.org/downloads/)
   - Verify installation:
     bash
     python --version
     
2. Ensure make is installed if you want to use the Makefile:
   - For Windows, you can use MinGW or Chocolatey.
   - For Linux/MacOS, make is typically pre-installed.

---

## *How to Run*

### **Option 1: Using the Makefile**

#### *Running the Server*
1. Open a terminal.
2. Navigate to the directory containing the Makefile, server.py, and client.py.
3. Run the server:
   bash
   make run_server
   

#### *Running the Client*
1. Open another terminal.
2. Navigate to the same directory.
3. Run the client:
   bash
   make run_client
   

#### *Cleaning Up Temporary Files*
To remove temporary files like __pycache__, run:
bash
make clean


#### *Help*
To display all available commands in the Makefile, run:
bash
make help


---

### *Option 2: Running Manually*

#### *Running the Server*
1. Open a terminal.
2. Navigate to the directory containing server.py.
3. Start the server:
   bash
   python server.py
   

#### *Running the Client*
1. Open another terminal.
2. Navigate to the directory containing client.py.
3. Start the client:
   bash
   python client.py
   

---

## *Usability Instructions*

### *Available Commands in the Client*
Once the client is connected to the server, the following commands can be used:
- **%groups**: List all available groups on the server.
- **%groupjoin <group_name>**: Join a specific group.
  bash
  %groupjoin public
  
- **%groupleave <group_name>**: Leave the current group.
  bash
  %groupleave public
  
- **%grouppost <group_name> <subject> <message>**: Post a message to a group.
  bash
  %grouppost public "Meeting" "Let’s discuss the agenda."
  
- **%groupusers <group_name>**: List all users in a specific group.
- **%groupmessage <group_name> <message_id>**: Retrieve a specific message from a group.
- **%exit**: Disconnect from the server and exit the chat.
- **%help**: Display a list of available commands and their usage.

---

## *Error Handling*

### *Known Issues and Solutions*
1. *Connection Refused*:
   - *Issue*: The client cannot connect if the server is not running.
   - *Solution*: Start the server before starting any clients.

2. *Server Crashes on Client Disconnection*:
   - *Issue*: Abrupt client disconnections may cause errors on the server.
   - *Solution*: Added exception handling to cleanly remove disconnected clients.

3. *JSON Formatting Errors*:
   - *Issue*: Messages improperly formatted as JSON.
   - *Solution*: Standardized message serialization and deserialization using Python’s json module.

4. *Group Membership*:
   - *Issue*: Users outside a group could previously access its messages.
   - *Solution*: Added validation to restrict access to group members only.

---

## *Example Usage*

### **Scenario: John and Alice Chat in public Group**

#### *John’s Terminal*
1. Start the client:
   bash
   python client.py
   
2. Enter alias:
   
   Choose an alias >>> John
   
3. Join the public group:
   
   %groupjoin public
   
4. Send a message:
   
   %grouppost public "Hello" "Hi everyone!"
   

#### *Alice’s Terminal*
1. Start the client:
   bash
   python client.py
   
2. Enter alias:
   
   Choose an alias >>> Alice
   
3. Join the public group:
   
   %groupjoin public
   