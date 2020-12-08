import time
import socket
from struct import pack, unpack
from threading import Thread


class connectionThread(Thread):
    global nicKToAddr

    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        while True:
            try:
                data = self.conn.recv(1024)
                msg = chr(data[0])
                print(msg)
                if msg == 'r':
                    register(data, self.addr)
                elif msg == 'd':
                    print("deregistering")
                    conn.close()
                    deregister(self)
                    break
            except socket.timeout:
                print('Socket timed out at', time.asctime())


def register(data, addr):
    nickname = unpack("30s", data[1:31])
    udpport = unpack("I", data[32:])
    nicKToAddr[nickname] = (addr[0], udpport)
    print(nicKToAddr[nickname])



def deregister(thread):
    connList.remove(thread)


MY_IP = '127.0.0.1'
MY_PORT = 50000

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.bind((MY_IP, MY_PORT))
print('Listening on Port ', MY_PORT, ' for incoming TCP connections')
sct.listen(5)

connList = []
nicKToAddr = {}

while True:
    try:
        conn, addr = sct.accept()
        thread = connectionThread(conn, addr).start()
        connList.append(thread)
    except socket.timeout:
        print('Socket timed out listening', time.asctime())

sct.close()
