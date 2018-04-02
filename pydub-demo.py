import hrtf
import pyaudio
import wave
from pydub import AudioSegment

aIndex = 0
eIndex = 8

CHUNK = 1024

hrtf.hrtf('audio/RiverStreamAdjusted.wav', aIndex, eIndex)
sound = AudioSegment.from_wav("hrtf.wav")
sound2 = AudioSegment.from_wav("hrtf.wav")
longSound = sound.append(sound2, crossfade=1500)
longSound.export("longSound.wav", format="wav")

# instantiate PyAudio
p = pyaudio.PyAudio()

wf = wave.open('longSound.wav', 'rb')

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
while len(data) > 0:

    # Play sound
    stream.write(data)

    # Read in buffered data
    data = wf.readframes(CHUNK)

# stop stream and PyAudio
stream.stop_stream()
stream.close()
wf.close()
p.terminate()
