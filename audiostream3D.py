import hrtf # used for 3D audio
import random
import pyaudio
from multiprocessing.pool import ThreadPool

class AudioStream3D:

    def __init__(self):
        # Config
        self.CHUNK = 65536 # 2^16
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 2
        self.FRAMERATE = 44100

        # Instantiate PyAudio
        p = pyaudio.PyAudio()

        # Instantiate a threading pool
        pool = ThreadPool(processes=1)

        # Open stream using callback
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=FRAMERATE, output=True)

        # Initialize current position in audio data and get first chunk
        currentPos = 0
        data_chunk = data[currentPos:currentPos + CHUNK]

        while True:
            # Asynchronously call HRTF thread
            async_result = pool.apply_async(HRTFUpdate, (aIndex, eIndex))

            # Play sound
            stream.write(data_chunk)

            # Update position in data
            currentPos += CHUNK

            # Retrieve the updated audio data
            try:
                data = async_result.get()
            except IndexError:
                break

            # Get new chunk of audio data to be streamed
            data_chunk = data[currentPos:currentPos + CHUNK]

        # Stop stream and PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

    def HRTFUpdate(aIndex, eIndex):
        """
        Updates the audio data based on the new azimuth and elevation of the user
        """
        soundToPlay = hrtf.hrtf('audio/RiverStreamAdjusted.wav', aIndex, eIndex)
        return soundToPlay.tobytes()

# Get line of sight elevation index and leftmost azimuth index
# Needs to be replaced with initial sensor data
eIndex = 8
aIndex = 0