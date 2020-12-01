import time
import socket
from struct import pack, unpack
import math

MY_IP = '127.0.0.1'
MY_PORT = 50000
server_activity_period = 30

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.bind((MY_IP, MY_PORT))
print('Listening on Port ', MY_PORT, ' for incoming TCP connections');

t_end = time.time() + server_activity_period

sct.listen(1)
print('Listening ...')

conn = None
addr = None

while time.time() < t_end:
    try:
        conn, addr = sct.accept()
        print('Incoming connection accepted: ', addr)
        break
    except socket.timeout:
        print('Socket timed out listening', time.asctime())

while time.time() < t_end:
    try:
        data = conn.recv(1024)

        if not data:
            print('Connection closed from other side')
            print('Closing ...')
            conn.close()
            break

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

        conn.send(data[0:4] + pack("i", ergebnis))
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sct.close()
if conn:
    conn.close()
