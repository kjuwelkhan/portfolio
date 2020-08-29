import socket
import threading
from pynput.mouse import Button, Controller
#import ctypes
import time
import sys

#ctypes.windll.shcore.SetProcessDpiAwareness(2)
execute = True
header = 16
format = "utf-8"
port = 3255
mouse  = Controller()


try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print(f"\nError thrown is {socket.error} (socket creation)")

try: 
    serverip = #your chosen ip
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
            print(targets)
            x = int(targets[0])
            y = int(targets[1])
            if (len(targets) == 4):
                button = targets[2]

                if button == "left": button = Button.left
                elif button == "right": button = Button.right
                print(targets[3])
                pressed = targets[3]
                if pressed == "False": pressed = False
                else: pressed = True

                print("Button is:", button)
                print("Pressed value is: ", pressed)
                mouse.position = (x,y)
                if pressed == True:
                    mouse.press(button)

                elif pressed == False:
                    mouse.release(button)
                

            elif (len(targets) == 2):
                mouse.position = (x,y)
            else: 
                raise Exception("Non valid input given")

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
