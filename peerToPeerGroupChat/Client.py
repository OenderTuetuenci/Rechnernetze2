import socket
from struct import pack,unpack

SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.connect((SERVER_IP,SERVER_PORT))

x = ""
msg = pack("c30sI",b'r',b'Matthias222',25525)
print(msg)
print(len(msg))
sct.send(msg)

msg = pack("c",b'd')
sct.send(msg)

while x != "q":
    x = input()