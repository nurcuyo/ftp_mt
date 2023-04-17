CNT4007
Nikolas Urcuyo 
UFID: 5450-8911
Project 2- FTP client and server with multiple threads

To use the program, first run the ftpserver.py program to start the server.

Then, run the command "python ftpclient.py 4007" (4007 is the port number).

After this, the client is prompted to enter a command to "get" a file from the server,
"upload" to the server, or "disconnect" from the server.

The "get" and "upload" commands prompt the client to send a filename. To upload to the server, 
the file must be in the client's directory. To get from the server, the file must be in the server's
directory. 

Multiple clients can be connected to the server and can upload and get files. 

Once a client is done, it should "disconnect" from the server.