import socket
import time
import pyaudio
import wave

 

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20002)
bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Send to server using created UDP socket
#time.sleep(200)

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

 

msgFromServer = UDPClientSocket.recvfrom(8192)
print("Received " + str(len(msgFromServer)) + " bytes...")

 

#msg = "Message from Server {}".format(msgFromServer[0])

#print(msg)


UDPClientSocket.close()
