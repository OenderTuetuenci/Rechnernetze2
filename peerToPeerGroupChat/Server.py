import time
import socket
from struct import pack, unpack
from threading import Thread


class connectionThread(Thread):
    global nicKToAddr
    global server
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.nickname = ""

    def run(self):
        while server:
            try:
                data = self.conn.recv(1024)
                print(data)
                msg = chr(data[0])
                print(msg)
                if msg == 'r':
                    register(data, self.addr,self)
                elif msg == 'd':
                    deregister(self.conn,self.nickname)
                    break
            except socket.timeout:
                print('Socket timed out at', time.asctime())
            except ConnectionResetError:
                deregister(self.conn,self.nickname)
        print("ending Thread ",self.nickname)

def inputThread():
    q = ""
    global server
    while q != "q":
        q = input()
        if q == "i":
            client_list_broadcast()
    server = False


def register(data, addr,thread):
    info = unpack("c30sI", data)
    nickname = info[1].decode("utf-8")
    thread.nickname = nickname
    if nickname in nicKToAddr.keys():
        string = "Nickname is taken"
        answer = pack("c?I17s",b'a',False,17,string.encode())
        conn.send(answer)
    else:
        nicKToAddr[nickname] = (addr[0], info[2])
        print("registered ",info[1])
        answer = pack("c?",b'a',True)
        conn.send(answer)
        client_list_broadcast()



def deregister(conn,nickname):
    connList.remove(conn)
    conn.close()
    nicKToAddr.pop(nickname)
    print("deregistering",nickname)
    client_list_broadcast()

def client_list_broadcast():
    #omega String bauen
    string=""
    for nickname,port in nicKToAddr.items():
        string = string + nickname + "," + str(port) + ";"
    for conn in connList:
        length = len(string)
        msg = pack("cI"+str(length)+"s",b'c',length,string.encode())
        conn.send(msg)
    print("Sended Clientlist Broadcast")



MY_IP = '127.0.0.1'
MY_PORT = 50001
server = True

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.bind((MY_IP, MY_PORT))
sct.settimeout(10)
print('Listening on Port ', MY_PORT, ' for incoming TCP connections')
sct.listen(5)

connList = []
nicKToAddr = {}

inputThread = Thread(target=inputThread).start()

while server:
    try:
        conn, addr = sct.accept()
        thread = connectionThread(conn, addr).start()
        connList.append(conn)
    except socket.timeout:
        print('Socket timed out listening', time.asctime())
sct.close()
