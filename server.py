import socket
import threading
import sys 
from pynput.mouse import Button, Controller

header = 8
format = "utf-8"
port = 3255
mouse  = Controller()

try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print(f"\nError thrown is {socket.error} (socket creation)")

try: 
    serverip = socket.gethostbyname(socket.gethostname())
except socket.gaierror():
    print(f"\nError thrown is {socket.gaierror()} (GAI)")
    sys.exit()

sock.bind((serverip, port))
sock.listen(5)

def handle_client(conn, addr):
    print(f"{addr} conncted to the server\n")
    while True:
        message_length = conn.recv(header).decode(format)
        if message_length != '': 
            message_length = int(message_length)
            message = conn.recv(message_length).decode(format)
            targets = message.split(' ')
            if (len(targets[0]) == 2):
                mouse.position(targets[0], targets[1])
                mouse.press(targets[2])
                mouse.release(targets[2])
            elif (len(targets[0]) == 1):
                mouse.position(targets[0], targets[1])
            else: 
                raise Exception("Non valid input given")
            print(f"[{addr}] {message}")
            if (message == "disconnect"):
                break
        
    conn.close()
sock.listen()

print(f"Server is listening on {serverip}\n")
while 1:
    (connectionsocket, address) = sock.accept()
    thread = threading.Thread(target=handle_client, args=(connectionsocket, address))
    thread.start()
    print(f"There are {threading.activeCount() - 1} connected\n")