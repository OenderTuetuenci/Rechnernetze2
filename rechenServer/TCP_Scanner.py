import threading
import socket
import time

SERVER = "141.37.168.26"
flag = True
sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.settimeout(1)

ports = [i for i in range(1,51)]

def scanPort(port):
    try:
        open = sct.connect_ex((SERVER, port))
        if open == 0:
            print("Port "+str(port)+" is open")
        else:
            print("Port " + str(port) + " is not open")
            ports.remove(port)
    except socket.timeout:
        print("Port " + str(port) + " is not open")
        ports.remove(port)

for i in ports:
    threading.Thread(target=scanPort, args=(i,)).start()

while True:
    x = input()
    if x == "end":
        flag = False
        break
sct.close()
print(ports)

