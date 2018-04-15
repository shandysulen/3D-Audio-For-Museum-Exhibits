import socket
import pyaudio
import wave
import time

HOST = '127.0.0.1'        # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Successfully connected with ' + HOST + '...')

s.sendall(b'1')
data = s.recv(8192)
print("Received " + str(len(data)) + " bytes...")

s.close()
