import pygame
import pyaudio
import wave
import sys
from bluetooth import discover_devices

class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()





def main():
    a = AudioFile("audio/RiverStreamAdjusted.wav")

    is_home = False
    print('Bluetooth Audio device search : My Device is JBL Micro Wireless')
    while True:
        print('Performing Bluetooth Search')

        nearby_devices = discover_devices(lookup_names=True)  #Searching for nearby Devices
        print('found {0} devices'.format(len(nearby_devices)))#printing all near by devices
        if nearby_devices:
            for address, name in nearby_devices:
                print(' {0} - {1}'.format(address, name))
                if name == 'JBL Micro Wireless':              #if the bluetooth headset name is this then gets connected and set its value true to play sound
                    is_home = True
                    break
            else:
                is_home = False

            if is_home:
                a.play()
                a.close()

            else:
                print('Not Playing')


if __name__ == '__main__':
    main()
