import socket
import sys

server = socket.gethostbyname(socket.gethostname())
port = int(sys.argv[-1])
format = 'utf-8'
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((server, port))
print("Connected to server...")

def upload(filename):
    c.send(b'upload')
    c.recv(0) #block to prevent multiple sends, headers be damned!
    c.send(filename.encode(format))
    c.recv(0)
    with open(filename, "rb") as f:
        print("Uploading...")
        while True:
            bread = f.read(1024)
            if bread == b"":
                c.send(str(0).encode(format))
                f.close()
                break
            strlen = str(len(bread)).encode(format)
            c.send(strlen + (b' ' * (128-len(strlen))))
            c.send(bread)
    print(f"Uploaded {filename} to the server.")

def get(filename):
    c.send(b'get')
    c.recv(0)
    c.send(filename.encode(format))
    c.recv(0)
    f = open("new" + filename, "wb")
    print("Downloading...")
    while True:
        breadamt = int(c.recv(128).decode(format))
        if breadamt == 0:
            f.close()
            break
        bread = c.recv(breadamt)
        f.write(bread)
    print(f"{filename} retrieved from server")

while True:
    print("Enter 'upload,' 'get', or 'disconnect' to interact with the server.")
    instruct = input()
    if instruct == "upload":
        print("Enter a filename to upload:", end = " ")
        upload(input())
    elif instruct == "get":
        print("Enter a filename to download:", end = " ")
        get(input())
    elif instruct == "disconnect":
        c.send(b"disconnect")
        print("Disconnected from server. Terminating session.")
        c.close()
        break
    else: 
        print("Invalid command.")
