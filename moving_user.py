import hrtf # used for 3D audio
import time
import random
import pyaudio
from pydub import AudioSegment
import wave

CHUNK = 32768 # 2^15

# Get line of sight elevation index and leftmost azimuth index
eIndex = 8
aIndex = 0

# instantiate PyAudio
p = pyaudio.PyAudio()

# create 3D audio file
hrtf.hrtf('audio/RiverStreamAdjusted.wav', aIndex, eIndex)

# open file
wf = wave.open('hrtf.wav', 'rb')

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# # set loop boolean flag
# loop = True

# Read in buffered data
data = wf.readframes(CHUNK)

currentPos = 0

# loop stream
while len(data) > 0:
    old_aIndex = aIndex
    old_eIndex = eIndex

    # Play sound
    stream.write(data)

    # Get position in data
    currentPos = wf.tell()
    print(currentPos)

    # Load the file with new azimuth and elevation
    r = random.random()
    if (r > 0.5):
        aIndex = old_aIndex + 1
    else:
        eIndex = old_eIndex + 3

    if aIndex != old_aIndex or eIndex != old_eIndex:
        hrtf.hrtf('audio/RiverStreamAdjusted.wav', aIndex, eIndex)
        # sound = AudioSegment.from_wav("hrtf.wav")
        # soundWithFadeIn = sound.fade_in(1000)
        # soundWithFadeIn.export("hrtf.wav", format="wav")
        wf = wave.open('hrtf.wav', 'rb')
        try:
            wf.setpos(currentPos)
        except wave.Error:
            print("Nearing end of data, could not update position")

    data = wf.readframes(CHUNK)

# stop stream and PyAudio
stream.stop_stream()
stream.close()
wf.close()
p.terminate()

# try instead of saving as a file, just keeping it in memory
