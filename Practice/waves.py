import thinkdsp

# Wave object contains:
#   1. ys = array that contains intensity values in the signal
#   2. ts = array of the times where the signal was evaluated or sampled
#   3. framerate = number of samples per unit of time

# Create sin and cos Signal objects which are really just math functions
cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)

# Sum the signals together
mix = sin_sig + cos_sig

# Evaluate the signal functions into a wave with a specified sample rate
wave = mix.make_wave(duration=0.5, start=0, framerate=11025)

# Create a new Wave object that contains the first three periods of the Signal object
period = mix.period
segment = wave.segment(start=0, duration=period*3)

# Plot
segment.plot()
thinkdsp.pyplot.show()

# Save the waveform as a Waveform Audio File (WAV)
wave.write(filename='output.wav')

# thinkdsp.play_wave(filename='output.wav', player='aplay') <---- replace aplay with another audio player

# Create audio spectrum as a Spectrum object from the Wave object
spectrum = wave.make_spectrum()

# Plot
spectrum.plot()
thinkdsp.thinkplot.show() # Wrapper

# Read in a .wav file and use it as a Wave object
water_wave = thinkdsp.read_wave('RiverStreamAdjusted.wav')
