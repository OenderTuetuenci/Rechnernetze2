import socket
from struct import pack, unpack
import threading
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 50001

UDP_Port = 25557

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('', UDP_Port))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER_IP, SERVER_PORT))

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('', UDP_Port))

run = True
# Registering
succes = False

while not succes:
    nickname = input("Nickname?")
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
            msg = unpack("cI", data[0:8])
            length = msg[1]
            msg = unpack("cI"+str(length)+"s",data)
            clientList(msg[2])
        except socket.timeout:
            print("Timeout")

def clientList(list):
    list = list.decode("utf-8")
    clients = list.split(";")
    for client in clients:
        if len(client) > 0:
            attr = client.split(",")
            print(attr[0]," UDP-Port: ", attr[1] + "," + attr[2])


listenServer = threading.Thread(target=listenServer).start()

x = ""
while x != "q":
    x = input()
run = False