import socket
from struct import pack, unpack

#SERVER_IP = '127.0.0.1'
SERVER_IP = "141.37.168.26"
#SERVER_PORT = 50000
SERVER_PORT = 7


sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sct.settimeout(10)

rechenopSum = "Summe".encode('utf-8')
rechenopProc = "Produkt".encode('utf-8')
rechenopMin = "Minimum".encode('utf-8')
rechenopMax = "Maximum".encode('utf-8')

id = pack("I", 1000)
rechenoperation = pack("7s", rechenopSum)
zahlN = pack("c", b'2')
zahlZ1 = pack("i", 10)
zahlZ2 = pack("i", 5)
zahlZ3 = pack("i", 100)
zahlZ4 = pack("i", -1)

rechenRequest_01 = id + rechenoperation + zahlN + zahlZ1 + zahlZ2
rechenoperation = pack("7s", rechenopProc)
rechenRequest_02 = id + rechenoperation + zahlN + zahlZ1 + zahlZ2
rechenoperation = pack("7s", rechenopMin)
zahlN = pack("c", b'4')
rechenRequest_03 = id + rechenoperation + zahlN + zahlZ1 + zahlZ2 + zahlZ3 + zahlZ4
rechenoperation = pack("7s", rechenopMax)
zahlN = pack("c", b'4')
rechenRequest_04 = id + rechenoperation + zahlN + zahlZ1 + zahlZ2 + zahlZ3 + zahlZ4


sct.sendto(rechenRequest_01, (SERVER_IP, SERVER_PORT))
ergebnis, addr = sct.recvfrom(1024)
#print(ergebnis)
idServer = unpack("I", ergebnis[0:4])
result = unpack("i", ergebnis[4:])

print("id: " + str(idServer[0]), "result: " + str(result[0]))


sct.sendto(rechenRequest_02, (SERVER_IP, SERVER_PORT))
ergebnis, addr = sct.recvfrom(1024)

idServer = unpack("I", ergebnis[0:4])
result = unpack("i", ergebnis[4:])

print("id: " + str(idServer[0]), "result: " + str(result[0]))

sct.sendto(rechenRequest_03, (SERVER_IP, SERVER_PORT))
ergebnis, addr = sct.recvfrom(1024)

idServer = unpack("I", ergebnis[0:4])
result = unpack("i", ergebnis[4:])

print("id: " + str(idServer[0]), "result: " + str(result[0]))

sct.sendto(rechenRequest_04, (SERVER_IP, SERVER_PORT))
ergebnis, addr = sct.recvfrom(1024)

idServer = unpack("I", ergebnis[0:4])
result = unpack("i", ergebnis[4:])

print("id: " + str(idServer[0]), "result: " + str(result[0]))