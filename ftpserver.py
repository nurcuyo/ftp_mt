import threading
import socket

server = socket.gethostbyname(socket.gethostname())
port = 4007
format = 'utf-8'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
print("Server started.")


def start():
    s.listen()
    while True:
        connection, address = s.accept()
        thread = threading.Thread(target=connect, args=(connection, address))
        thread.start()
        print(f"Clients currently active: {threading.active_count()-1}")


def connect(connection, address):
    print(f"Connected to {address}...")
    while True:
        instruct = connection.recv(4096).decode(format)
        connection.send(b'') #blocks to prevent recv-ing multiple sends

        if instruct == "upload":
            print(f"Client {address} is uploading...")
            filename = connection.recv(4096).decode(format)
            connection.send(b'')
            print(filename)
            f = open("new" + filename, "wb")
            print("Downloading...")
            while True:
                breadamt = int(connection.recv(128).decode(format))
                if breadamt == 0:
                    f.close()
                    break
                bread = connection.recv(breadamt)
                f.write(bread)
            print(f"Downloaded {filename} from client {address}.")
        
        elif instruct == "get":
            print(f"Client {address} is downloading...")
            filename = connection.recv(4096).decode(format)
            connection.send(b'')
            print(filename)
            with open(filename, 'rb') as f:
                while True:
                    bread = f.read(1024)
                    if bread == b"":
                        connection.send(str(0).encode(format))
                        f.close()
                        break
                    strlen = str(len(bread)).encode(format)
                    connection.send(strlen + (b' ' * (128-len(strlen))))
                    connection.send(bread)
            print(f"Uploaded {filename} to client {address}.")
        
        elif instruct == "disconnect":
            print(f"Client {address} disconnected from the server.")
            print(f"Clients currently active: {threading.active_count()-2}")
            break

        else:
            print("Invalid command.")
        
        instruct = ''

start()
