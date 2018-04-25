import hrtf # used for 3D audio
import random
import pyaudio
from multiprocessing.pool import ThreadPool
import time

class AudioStream3D:

    def __init__(self):
        # Config
        self.CHUNK = 65536 # 2^16
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 2
        self.FRAMERATE = 44100
        self.audiofile = None

        # Instantiate PyAudio
        p = pyaudio.PyAudio()

        # Instantiate a threading pool
        pool = ThreadPool(processes=1)

        # Open stream using callback
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.FRAMERATE, output=True)

        # Initialize current position in audio data and get first chunk
        currentPos = 0

        data_chunk = [0] * self.CHUNK

        isLooping = True
        print("shando")
        while isLooping:
            print("1")
            time.sleep(1)
            while self.audiofile != None:
                # Asynchronously call HRTF thread
                async_result = pool.apply_async(self.HRTFUpdate)

                print("yo")

                # Play sound
                stream.write(data_chunk)

                # Update position in data
                currentPos += self.CHUNK

                # Retrieve the updated audio data
                try:
                    data = async_result.get()
                except IndexError:
                    break

                # Get new chunk of audio data to be streamed
                data_chunk = data[currentPos:currentPos + self.CHUNK]

                isLooping = False
            print("2")
            time.sleep(1)
        # Stop stream and PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("3")

    def setAudioFile(self, audiofile):
        print("bless")
        self.audiofile = audiofile

    def HRTFUpdate(self):
        """
        Updates the audio data based on the new azimuth and elevation of the user
        """
        soundToPlay = hrtf.hrtf(self.audiofile, random.randint(0,24), 8)
        return soundToPlay.tobytes()
