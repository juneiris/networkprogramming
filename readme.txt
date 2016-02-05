What's in the folder:
1.server side programm--Server.py
2.client program--Client.py
3.user_pass.txt: contains the valid combination of usernames and passwords
4.readme.txt:describes running instruction and general infomation of code



Develop environment:
Server.py and Client.py are developed in python 2.7.2.



Brief description of code:
server program Server.py can support multiple clients, mainly deals with functionalities of clients authentication(including block), message transmission between clients. Initially, its ip address is set to be localhost, and its port number can be assigned by user.
It should be run first as follow: python path/Server.py portnumber.
for example:python path/Server.py 8001
before running it, be sure to change the path of user_pass.txt in the program to read the txt file correctly because now in the program the path is absolute path in my own computer.

one Client.py can support one client, it can send out messages and receive messages from server, it also takes charge of TIME_OUT function.
Client.py can be run as follow: python  path/Client.py  server's ip  server's port
for example: python path/Client.py localhost 8001.
the Client.py needs to know server's ip address and port number before execution, it's not able to obtain them automatically.



Instruction to run code:

there is no makefile, simply type python <path/Server.py><port> first and then python <paht/Client.py><host><port> in terminal.

invoke pragrams:
if test with one computer:
the ip address is set to be localhost.
Server.py:python path/Server.py 8001. Client.py:python path/Client.py localhost 8001.
if test with multiple computers:
change ip address and in Server.py first, type in port number to invoke serverprogram. And type in the same ip address and port number to invoke Client.py. The Client.py needs to know server's ip address and port number before execution, it's not able to obtain them automatically.

login:
type in username and password in Client.py, and follow the suggestions on screen. login failure times is defined as FAILURE_TIME and it is set to be three. Three times failure in the same connection are allowed for each username, or the username will be blocked in this ip address, It means current connection will be close, and the username will not be able to login again from this ip in BLOCK_TIME. Notice that even if the username is not vaild in list, it will also be blocked. when BLOCK_TIME passes, the username needs to relogin. Duplicate users are not allowed.

input commands:
type in commands in Client.py after login. the server can only recognize the provided commands listed in table 1 in instruction. Note that when broadcast to all users, user who send message will not receive the message. If a user try send messages to other users that are not online, a suggestion will appear to ask the user to change receiver.
***: private talk and broadcast functions all work fine when there is no suddenly logout, but  when two users are having conversation, A is sending B a message and B suddenly logout, sometimes an attribute error happen will happen. In this case, the server will send A a meesage to ask it to logout and login again.

logout:
when client sends out logout request, it will receive a goodbye message from server(server connection close), and it has to press ENTER to logout thoroughly(close its socket).

timout:
TIME_OUT is defined in Client.py, for the purpose of testing, it is set to be one(minutes) instead of 30. If the client has no input for TIME_OUT time, the client will receive a goodbye message from server and its connection will closed by server. Also, client need to press ENTER to close its own socket.

Keybroad Interrupt(Crtl+C): 
when server has a keybroad Interrruption, it will send goodbye message(close connection) to all clients. when a client has a Keybroad Interruption, it will send 'logout' message to server to let server close the connection before it closes its socket.

Locations that define variables:
user_pass.txt will be open in Server.py
BLOCK_TIME and login failure times FAILURE_TIME are defined in Server.py
TIME_OUT is defined in Client.py






