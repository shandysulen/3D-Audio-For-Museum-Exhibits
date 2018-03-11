import thinkdsp
import scipy.io as scp
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

# Reads in a .wav file into a Wave object with frame rate of 44.1k Hz
waveform = thinkdsp.read_wave('RiverStreamAdjusted.wav')
samplerate = waveform.framerate

# Reads in the HRTF database data file
hrtf_db = scp.loadmat('CIPIC_58_HRTF.mat')

# 25 azimuth locations according to CIPIC
azimuths = [-80, -65, -55, -45, -40,
            -35, -30, -25, -20, -15,
            -10, -5, 0, 5, 10,
            15, 20, 25, 30, 35,
            40, 45, 55, 65, 80]

# 50 elevation locations according to CIPIC
elevations = np.arange(-45, 230.625, 5.625)

# Choose arbitrary azimuth and elevation
aIndex = 18 # to the right
eIndex = 17 # above

# Extract hrir's from the HRTF database
hrir_l = hrtf_db['hrir_l']
hrir_r = hrtf_db['hrir_r']

# Get head-related impulse samples
rgt = list(np.squeeze(hrir_r[aIndex][eIndex][:]))
lft = list(np.squeeze(hrir_l[aIndex][eIndex][:]))

# Plot
plt.plot(rgt, 'r', label='Right Ear')
plt.plot(lft, 'b', label='Left Ear')
plt.ylabel('Intensity (db)')
plt.xlabel('Time')
plt.title('Head Related Impulse Response (HRIR)')
plt.legend()
plt.show()

# Generate ITD (Interaural Time Difference) | this isn't MATLAB
delay = hrtf_db['ITD'][aIndex - 1][eIndex - 1]
zeros_delay = [0] * abs(int(delay))

#Include the delay in left and right stereo channels
if aIndex < 13:
    lft = lft + zeros_delay
    rgt = zeros_delay + rgt
else:
    lft = zeros_delay + lft
    rgt = rgt + zeros_delay

# Perform convolution
left_convolved = list(np.convolve(waveform.ys, lft))
right_convolved = list(np.convolve(waveform.ys, rgt))
zeros_samplerate = [0] * int(samplerate * 0.2)

print("Left_convolved length", len(left_convolved))
print("Right_convolved length", len(right_convolved))

# Include convolved audio in left and right stero channels
wav_left = left_convolved + zeros_samplerate
wav_right = right_convolved + zeros_samplerate

print("Type of wav_left:", type(wav_left))
print("Type of wav_right:", type(wav_right))
print("Size of wav_left:", len(wav_left))
print("Size of wav_right:", len(wav_right))

# Create np array soundToPlay with wav_left and wav_right
soundToPlay = np.array([wav_left, wav_right])

print("Type of soundToPlay:", type(soundToPlay))
print("Size of soundToPlay:", len(soundToPlay))

# Play 3D audio!
sd.play(soundToPlay.T, samplerate) # not playing sounds ?!?!?!?!

print("Reached successful termination of program")
