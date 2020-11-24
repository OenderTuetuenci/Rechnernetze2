import base64
import socket

recvBytes = 10000
enter = "\r\n".encode()
mailFrom = "fakemail@fake.com".encode()
mailTo = "matthreich@gmail.com".encode()
msgHeader = "FROM:".encode() + mailFrom + enter + "TO:".encode() + mailTo + enter + "SUBJECT:".encode() + "Wunerschönen Tag wünsche ich".encode() + enter + enter
msgText = "Hallo, dies ist eine tolle Nachricht an einen tollen Typen aus einem Python-Skript!!".encode() + enter
msgEnd = ".".encode() + enter
message = msgHeader + msgText + msgEnd

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.settimeout(10)

sct.connect(('141.37.11.129', 587))
print(sct.recv(recvBytes).decode())

sct.send("AUTH LOGIN\r\n".encode())
msg = sct.recv(recvBytes).decode().split(" ")
msg2 = base64.b64decode(msg[1])
print(str(msg[0]) + " " + str(msg2))

sct.send((base64.b64encode('rnetin'.encode('utf-8'))) + enter)
print(sct.recv(recvBytes).decode())

sct.send((base64.b64encode('ntsmobil'.encode('utf-8'))) + enter)
print(sct.recv(recvBytes).decode())

sct.send("MAIL FROM:".encode() + mailFrom + enter)
print(sct.recv(recvBytes).decode())

sct.send("RCPT TO:".encode() + mailTo + enter)
print(sct.recv(recvBytes).decode())

sct.send("DATA".encode() + enter)
print(sct.recv(recvBytes).decode())

sct.send(message)
print(sct.recv(recvBytes).decode())

sct.close()
