import sounddevice as sd
import soundfile as sf

data, fs = sf.read('RiverStreamAdjusted.wav', dtype='float32')
sd.play(data, fs)
status = sd.wait()

print("Program completed execution")
