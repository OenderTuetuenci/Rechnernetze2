import socket
from struct import pack, unpack
import threading
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 50001

UDP_Port = 25552
CHAT_IP = '127.0.0.1'
CHAT_Port = 60002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER_IP, SERVER_PORT))

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('', UDP_Port))

chat = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
chat.bind((CHAT_IP,CHAT_Port))

run = True
# Registering
succes = False

while not succes:
    nickname = input("Nickname?\n")
    msg = pack("c30sI", b'r', nickname.encode(), UDP_Port)
    server.send(msg)
    data = server.recv(1024)
    answer = data[1]
    if answer == 1:
        succes = True
    else:
        msg = unpack("c?I17s", data)
        print(msg[3].decode("utf-8"))

def listenServer():
    global run
    while run:
        try:
            data = server.recv(10000)
            if unpack("c",data[0:1])[0].decode("utf-8") == "c":
                msg = unpack("cI", data[0:8])
                length = msg[1]
                msg = unpack("cI"+str(length)+"s",data)
                clientList(msg[2])
        except socket.timeout:
            print("Timeout")

def listenudp():
    global run
    global connected
    while run:
        try:
            data = udp.recv(1024)
            msg = unpack("cI",data[0:8])
            length = msg[1]
            msg = unpack("cI"+str(length)+"s",data)
            ip = msg[2].decode('UTF-8')
            ip = ip.split(",")
            chat.connect((ip[0],int(ip[1])))
            threading.Thread(target=chatf,args=(chat,)).start()
            connected = True
        except socket.timeout:
            print("Timeout")

def clientList(list):
    list = list.decode("utf-8")
    clients = list.split(";")
    for client in clients:
        if len(client) > 0:
            attr = client.split(",")
            print(attr[0]," UDP-Port: ", attr[1] + "," + attr[2])

def listenChat(conn):
    while True :
        try:
            data = conn.recv(1024)
            answer = unpack("cI", data[0:8])
            length = answer[1]
            answer = unpack("cI" + str(length) + "s", data)
            print("Antwort:",answer[2].decode("UTF-8"))
            if answer[2].decode("UTF-8") == "end chat":
                conn.close()
                break
        except socket.timeout:
            print("Timeout")
    print("Ending Chat Thread")

def chatf(conn):
    global connected
    conn.send(b'Chat startet')
    data = conn.recv(1024)
    print(data)
    threading.Thread(target=listenChat, args=(conn,)).start()
    x = ""
    while x != "end chat":
        x = input("Nachricht:\n")
        length = len(x)
        msg = pack("cI"+str(length)+"s",b'm',length,x.encode())
        conn.send(msg)
    connected = False
    conn.close()


def sendConnectWithUser():
    global chat
    user = input("Welchen User? IP,Port\n")
    print(user)
    info = user.split(",")
    port = int(info[1])
    data = CHAT_IP + "," + str(CHAT_Port)
    msglen = len(data)
    msg = pack("cI"+str(msglen)+"s",b'm',msglen,data.encode())
    udp.sendto(msg,(info[0],port))
    chat.listen(5)
    try:
        conn,addr = chat.accept()
        threading.Thread(target=chatf,args=(conn,)).start()
    except socket.timeout:
        print("Timeout")

def deregister():
    msg = pack("c",b'd')
    server.send(msg)
    server.close()



listenServer = threading.Thread(target=listenServer).start()
listenUDP = threading.Thread(target=listenudp).start()

x = ""
connected = False
while x != "q":
    if not connected:
        x = input("::")
    if x == "connect":
        sendConnectWithUser()
        connected = True
        x = ""
    if x == "deregister":
        deregister()
        x = ""
run = False