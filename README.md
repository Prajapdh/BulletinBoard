#  Bulletin Board Project Using Socket Programming

## Team Members
- **Daksh Prajapati**
- **Arya Narke**
- **Varad Parte**

## Project Overview
This project implements a multithreaded bulletin board using client-server architecture. It allows users to create, join, and interact with groups. The server manages group memberships and messages, while the client application provides a user-friendly interface to execute commands.


## How to Compile and Run the Project

### **PREREQUISITES**
Ensure that you have the following installed on your system:
- Python 3.x

### **STEPS TO RUN**
1. **Download the Required Files**
   - Ensure you have the `server.py` and `client.py` files in the same directory.

2. **Run the Server**
   - Open a terminal or command prompt.
   - Navigate to the directory containing `server.py`.
   - Execute the following command to start the server:
     ```
     python server.py
     ```
   - The server will start listening on `127.0.0.1` (localhost) and port `8080`.

3. **Run the Client**
   - Open another terminal or command prompt.
   - Navigate to the directory containing `client.py`.
   - Execute the following command to start the client:
     ```
     python client.py
     ```
   - Follow the prompts to choose a username and begin interacting with the bulletin board. 

4. **Optional - Run GUI Client**
   - Execute the following command to start the client with an interactive UI: 
     ```
     python GUIclient.py
     ```
     - **Please make the window FULL SCREEN to view all buttons.**

### Commands Available in the Client
Users can use the following commands:
- `%groups` - List all available groups
- `%groupjoin <group_name>` - Join a specific group
- `%groupleave <group_name>` - Leave a specific group
- `%grouppost <group_name> <subject> <message>` - Post a message to a specific group
- `%groupusers <group_name>` - List users in a specific group
- `%groupmessage <group_name> <message_id>` - Retrieve a specific message
- `%join` - Join the public group
- `%post <subject> <message>` - Post a message to the public group
- `%users` - List users in the public group
- `%leave` - Leave the public group
- `%message <message_id>` - Retrieve a specific message from the public group
- `%exit` - Exit the chat
- `%help` - Show the list of commands


## Usability Instructions
The system is designed to handle multiple clients connecting to the server concurrently. Users must ensure the server is running before connecting clients. If a client disconnects abruptly, their data might not be saved.

## Issues Encountered and Their Solutions

**1. Group Join and Leave Mechanism**

*Issue:* The join group and leave group functions had issues with message handling synchronization, resulting in some users not receiving messages intended for the group.

*Solution:* Implemented broadcast function to ensure all users in the group are notified correctly and added error-handling functions to address synchronization problems.

**2. Unauthorized Access**

*Issue:* Users not in a group were able to retrieve its messages and view the list of users.

*Solution:* Added error-handling functions to validate group membership before granting access and implemented broadcast messages to notify users about unauthorized attempts.

**3. Handling Disconnections**

*Issue:* Clients disconnecting abruptly caused errors on the server side.

*Solution:* Implemented exception handling to gracefully remove disconnected clients and clean up resources.

**4. Command Validation**

*Issue:* Clients occasionally sent invalid or incomplete commands, leading to server errors.

*Solution:* Added command parsing and validation on both client and server sides.

---

