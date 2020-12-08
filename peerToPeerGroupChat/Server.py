import time
import socket
from struct import pack, unpack
import math
import threading


def handleMessage():
    try:
        while True:
            data = conn.recv(1024)

            if data:
                sendMessage(data)
                id = unpack("I", data[0:4])[0]
            else:
                print('Connection closed from other side')
                print('Closing ...')
                connList[id - 1].close()
                connList.remove(id - 1)
                break
    except socket.timeout:
        print('Socket timed out at', time.asctime())


def sendMessage(data):
    print('received message: ', data, 'from ', addr)
    connList[id[0] - 1].send(data[0:4] + pack("i", ergebnis))


MY_IP = '127.0.0.1'
MY_PORT = 50000

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.bind((MY_IP, MY_PORT))
print('Listening on Port ', MY_PORT, ' for incoming TCP connections')

sct.listen(5)
print('Listening ...')

conn = None
addr = None

connList = []

input = ""
while input != "q":
    try:
        conn, addr = sct.accept()
        print('Incoming connection accepted: ', addr)
        connList.append(conn)
        threading.Thread(target=handleMessage).start()

    except socket.timeout:
        print('Socket timed out listening', time.asctime())

    input = input()

sct.close()
for x in connList:
    x.close()


class connectionThread(Thread):

    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        while True:
            try:
                data = self.conn.recv(1024)



            except socket.timeout:
                print('Socket timed out at', time.asctime())
