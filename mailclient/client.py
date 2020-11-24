import base64
import socket

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sct.settimeout(10)

sct.connect(('141.37.11.129', 587))
print(sct.recv(10000).decode())

sct.send("AUTH LOGIN\r\n".encode())
msg = sct.recv(10000).decode().split(" ")
msg2 = base64.b64decode(msg[1])
print(str(msg[0]) + " " + str(msg2))

sct.send((base64.b64encode('rnetin'.encode('utf-8'))) + "\r\n".encode())
print(sct.recv(10000).decode())

sct.send((base64.b64encode('ntsmobil'.encode('utf-8'))) + "\r\n".encode())
print(sct.recv(10000).decode())

mailFrom = "fakemail@fake.com".encode()
mailTo = "matthreich@gmail.com".encode()
enter = "\r\n".encode()

sct.send("MAIL FROM:".encode() + mailFrom + enter)
print(sct.recv(10000).decode())

sct.send("RCPT TO:".encode() + mailTo + enter)
print(sct.recv(10000).decode())

sct.send("DATA".encode() + enter)
print(sct.recv(10000).decode())

message = "FROM:".encode() + mailFrom + enter + "TO:".encode() + mailTo + enter + "SUBJECT:".encode() + "Wunerschönen Tag wünsche ich".encode() + enter + enter + "Hallo, dies ist eine tolle Nachricht an einen tollen Typen aus einem Python-Skript!!".encode() + enter + ".".encode() + enter

sct.send(message)
print(sct.recv(10000).decode())

sct.close()
