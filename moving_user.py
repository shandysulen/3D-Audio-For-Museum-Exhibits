import hrtf # used for 3D audio
import time
import random
import pyaudio
import wave

CHUNK = 512

# Get line of sight elevation index and leftmost azimuth index
eIndex = 8
aIndex = 0

# instantiate PyAudio
p = pyaudio.PyAudio()

# create 3D audio file
hrtf.hrtf('audio/plantain_frying_mono.wav', aIndex, eIndex)

# open file
wf = wave.open('hrtf.wav', 'rb')

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read initial data
data = wf.readframes(CHUNK)

# set loop boolean flag
loop = True

# loop stream
while loop:

    # Play sound
    stream.write(data)

    # Read in buffered data
    data = wf.readframes(CHUNK)

    # Load the file with new azimuth and elevation
    if len(data) == 0:
        r = random.random()
        aIndex = aIndex + 3 if (r > 0.5) else eIndex + 3
        hrtf.hrtf('audio/plantain_frying_mono.wav', aIndex, eIndex)
        wf = wave.open('hrtf.wav', 'rb')
        data = wf.readframes(CHUNK)

# stop stream and PyAudio
stream.stop_stream()
stream.close()
wf.close()
p.terminate()
