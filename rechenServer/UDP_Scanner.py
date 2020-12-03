import threading
import socket

SERVER = "141.37.168.26"
flag = True
sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sct.settimeout(5)

ports = [i for i in range(1,51)]

def scanPort(port):
    try:
        sct.sendto(b'Hallo',(SERVER,port))
        msg = sct.recv(1000)
        print(msg)
    except socket.timeout:
        print(str(port)+" is not open")
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