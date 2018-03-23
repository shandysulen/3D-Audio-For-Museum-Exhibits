import scipy.io as scp # used to load .mat file
import numpy as np # used for multi-dimensional array
import soundfile as sf # used to save .wav file
import sys

def hrtf(fileName, aIndex, eIndex):
    """
    This function will save a 3D audio version of the fileName by computing
    the head-related transfer function based off the passed-in azimuth
    and elevation indices

    Arguments:
    fileName - a string of the filename which the user wants 3D audio playback of
    aIndex - the index of the azimuth list that returns the desired azimuth
    eIndex - the index of the elevation list that returns the desired elevation
    """
    # Reads in a .wav file into a Wave object with frame rate of 44.1k Hz
    try:
        data, fs = sf.read(fileName, dtype='float32')
    except RuntimeError:
        print("Error: Audio file cannot be played, or it doesn't exist.")
        sys.exit(0)

    # Reads in the HRTF database data file
    try:
        hrtf_db = scp.loadmat('CIPIC_58_HRTF.mat')
    except RuntimeError:
        print("Error: Audio file cannot be played, or it doesn't exist.")
        sys.exit(0)

    # Convert stereo audio file to mono by grabbing the left channel only
    if len(data.shape) == 2:
        data = data[:][0]

    # Extract hrir's from the HRTF database
    hrir_l = hrtf_db['hrir_l']
    hrir_r = hrtf_db['hrir_r']

    # Get head-related impulse samples
    rgt = list(np.squeeze(hrir_r[aIndex][eIndex][:]))
    lft = list(np.squeeze(hrir_l[aIndex][eIndex][:]))

    # Generate ITD (Interaural Time Difference) | this isn't MATLAB
    delay = hrtf_db['ITD'][aIndex - 1][eIndex - 1]
    zeros_delay = [0] * abs(int(delay))

    # Include the delay in left and right stereo channels
    if aIndex < 13:
        lft = lft + zeros_delay
        rgt = zeros_delay + rgt
    else:
        lft = zeros_delay + lft
        rgt = rgt + zeros_delay

    # Perform convolution
    left_convolved = list(np.convolve(data, lft))
    right_convolved = list(np.convolve(data, rgt))
    zeros_samplerate = [0] * int(fs * 0.2)

    # Include convolved audio in left and right stero channels
    wav_left = left_convolved + zeros_samplerate
    wav_right = right_convolved + zeros_samplerate

    # Create np array soundToPlay with wav_left and wav_right
    soundToPlay = np.array([wav_left, wav_right], dtype='float32')

    # Find max between left and right stereo channels
    maxlft = max(soundToPlay[0])
    maxrgt = max(soundToPlay[1])
    if (maxlft > maxrgt):
        maximum = maxlft
    else:
        maximum = maxrgt

    # Scale the wave to -1 and 1
    soundToPlay = soundToPlay / float(maximum)

    # Transpose multi-dimensional array into the proper shape
    soundToPlay = soundToPlay.T

    # Save 3D audio file for playback
    sf.write('hrtf.wav', soundToPlay, fs)

# start with 5 ft as the cutoff for the sounds
# to get multiple sounds, just add the left channels with one another and
# add the right channels with one another and output that
