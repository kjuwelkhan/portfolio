import socket
import time
from pynput import *
import sys
import pyautogui

header = 16
format = "utf-8"
port = 3255
server = #your chosen ip here
clientSysWidth = str(pyautogui.size()[0])
clientSysHeight = str(pyautogui.size()[1])

clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsock.connect((server, port))
print("connected")

def send(msg):
    message = msg.encode(format)
    message_length = str(len(message)).encode(format)
    message_length += b' ' * (header - len(message_length))
    clientsock.send(message_length)
    clientsock.send(message)

#Track cursor definitions
def track_cursor(x, y):
    send(str(x) + " " + str(y))

def on_click(x, y, button, pressed):
    #send("{0} at {1}".format('Pressed' if pressed else 'Released', (x,y)))
    print(button)
    print(pressed)
    if str(button) == "Button.right":
        button = "right"

    if str(button) == "Button.left":
        button = "left"
    
    send(str(x) + " " + str(y) + " " + button + " " + str(pressed))

send(clientSysWidth + " " + clientSysHeight + " <- Here Is The System Resolution")

with mouse.Listener(on_move = track_cursor,on_click = on_click) as hlhook:
    hlhook.join()

send("disconnect")
