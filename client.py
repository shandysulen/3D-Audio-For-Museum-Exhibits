import socket
import pyaudio
import wave
import time

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
frames = []

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Successfully connected with ' + HOST + '...')

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    print("Entered callback...")
    s.sendall(b'1')
    data = s.recv(8192)
    print("Received " + str(len(data)) + " bytes...")
    return (data, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                stream_callback = callback)

print('Starting stream...')
stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

print('Closing stream...')
stream.stop_stream()
stream.close()
p.terminate()
s.close()
