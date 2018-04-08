# first of all import the socket library
import socket
import random
import pyaudio
import hrtf
 
# next create a socket object
s = socket.socket()         
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

sendThis = hrtf.hrtf('audio/RiverStreamAdjusted.wav', aIndex, eIndex)
data = sendThis.tobytes()

 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)     
print ("socket is listening" )          
 
# a forever loop until we interrupt it or 
# an error occurs
while True:
 
   # Establish connection with client.
   c, addr = s.accept()     
   print ('Got connection from', addr)
   c.send(data)

       
       


   # send a thank you message to the client. 
   
 
   # Close the connection with the client
   c.close()
