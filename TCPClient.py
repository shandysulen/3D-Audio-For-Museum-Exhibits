import socket
import time

HOST = '10.0.1.12'        # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Successfully connected with ' + HOST + '...')

while True:
    s.sendall(b'1')
    data = s.recv(8192)
    print("Received " + str(len(data)) + " bytes...")
    print(str(time.time()) + ": " + data.decode("utf-8"))

s.close()
