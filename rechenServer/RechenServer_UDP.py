import socket
import time
from struct import pack, unpack
import math

My_IP = "127.0.0.1"
My_PORT = 50000
server_activity_period = 30

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((My_IP, My_PORT))

sock.settimeout(10)
t_end = time.time() + server_activity_period

while time.time() < t_end:
    try:
        data, addr = sock.recvfrom(1024)

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

        sock.sendto(data[0:4] + pack("i", ergebnis), addr)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sock.close()
