import socket
import time
import random
import pyaudio
import hrtf

 

localIP     = "127.0.0.1"

localPort   = 20002

bufferSize  = 8192

 

msgFromServer= "Hello UDP Client"
eIndex = 8
aIndex = 0
sendThis = hrtf.hrtf('RiverStreamAdjusted.wav', aIndex, eIndex)
data_sound = sendThis.tobytes()
bytesToSend= str.encode(msgFromServer)

 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")
#time.sleep(100)
 

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

   

    # Sending a reply to client

    UDPServerSocket.sendto(data_sound, address)
    time.sleep(3)





UDPServerSocket.close()
