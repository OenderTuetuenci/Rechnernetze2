import time
import socket
from struct import pack, unpack
import math
import threading

def rl(sock):
    n=0
    c=1
    while c:
        c=sock.recv(1)
        print(c)
        if c==b'\n':
            return n
        n+=1
    return ''

def handleMessage():
    try:
        while True:
            print(rl(conn))
            data = conn.recv(1014)

            if data:
                sendMessage(data)
                id = unpack("I", data[0:4])[0]
            else:
                print('Connection closed from other side')
                print('Closing ...')
                connList[id-1].close()
                connList.remove(id-1)
                break
    except socket.timeout:
        print('Socket timed out at', time.asctime())

def sendMessage(data):
    id = unpack("I", data[0:4])
    rechop = unpack("7s", data[4:11])
    number = unpack("c", data[11:12])
    zahlen = unpack(number[0].decode() + "i", data[12:])

    ergebnis = 0

    if rechop[0].decode() == "Produkt":
        ergebnis = math.prod(zahlen)
    elif rechop[0].decode() == "Minimum":
        ergebnis = min(zahlen)
    elif rechop[0].decode() == "Maximum":
        ergebnis = max(zahlen)
    elif rechop[0].decode() == "Summe\x00\x00":
        ergebnis = sum(zahlen)

    print('received message: ', data, 'from ', addr)
    connList[id[0]-1].send(data[0:4] + pack("i", ergebnis))


MY_IP = '127.0.0.1'
MY_PORT = 50001
server_activity_period = 30

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.bind((MY_IP, MY_PORT))
print('Listening on Port ', MY_PORT, ' for incoming TCP connections');

t_end = time.time() + server_activity_period

sct.listen(5)
print('Listening ...')

conn = None
addr = None

connList = []

while time.time() < t_end:
    try:
        while True:
            conn, addr = sct.accept()
            print('Incoming connection accepted: ', addr)
            connList.append(conn)
            threading.Thread(target=handleMessage).start()

    except socket.timeout:
        print('Socket timed out listening', time.asctime())


sct.close()
for x in connList:
    x.close()
