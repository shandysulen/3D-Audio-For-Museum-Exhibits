from marvelmind import MarvelmindHedge
from time import sleep
import socket
import sys

# Globals
HOST = ''      # Symbolic name meaning all available interfaces
PORT = 50007   # Arbitrary non-privileged port

# Instantiate hedge location tracking
hedge = MarvelmindHedge(tty="/dev/ttyACM0")  # create MarvelmindHedge thread
hedge.start()  # start thread

# Set up TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("Server listening on port 50007...")

# Accept client connection
conn, addr = s.accept()
print('Successfully connected with ' + addr[0] + '...')

iterations = 100

# Continue waiting for client input
while iterations > 0:

    print("Iteration #" + str(iterations) + ":")

    try:
        # Client asks for location data
        data = conn.recv(1024)
        print("Data Received:", data)
        if data == b'1':

            # Server sends location data
            # print("valuesImuRawData:", hedge.valuesImuRawData())
            position_list = hedge.position()[1:3]
            print("Position List:", position_list)
            position_str = str(position_list[0]) + ", " + str(position_list[1])
            print(position_str)
            conn.sendall(position_str.encode(encoding='UTF-8',errors='strict'))
    except Exception as e:
        print(e)
        conn.close()
        s.close()

    iterations -= 1

# Close TCP connection and socket
conn.close()
s.close()

# Stop hedge's infinite loop
hedge.stop()
