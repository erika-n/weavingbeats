#!/usr/bin/python
import numpy as np

import wave
import scipy.io.wavfile as wav
from pprint import pprint
from scipy.special import expit
import sys
f = 1.0/32767
def get_sound_data(wav_name):

    # Read in
    data = wav.read(wav_name)
    rate = data[0]
    data = data[1]/2
    data = data.astype(np.float32)
    data = data/(2*np.max(data)) #normalize

    # Convert to mono

    if(data.ndim > 1):
        data = np.sum(data, axis=1)
    #data = f*data
    # data += f*32767

    return data



def save_wav(data, name):
    #data = 25000.0*data #back to int
    # data -= f*32767
    # data = data/f
    data = 20000*data
    data = np.int16(data)

    seconds = len(data)/44100.0
    print ("seconds = " + str(seconds))
    print(data[:100])

    # Write to disk
    z = np.zeros(data.shape, dtype=np.int16)
    data = np.append(data, z)
    output_file = wave.open(name, "w")
    output_file.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
    output_file.writeframes(data)
    output_file.close()

    print "Wrote " + name


def envelope(num, attack, decay):

    if(num < attack + decay):
        attack = num/2
        decay = num - attack -1 

    start = [-6 + 12*x*1.0/attack  for x in range(int(attack))] 
    end = [ 6 -12*x*1.0/decay  for x in range(int(decay))]
    if(num >= attack + decay):
        mid = np.empty(int(num - attack - decay))
        mid.fill(6.0)
        total = np.append(start, mid)
    else:
        total = start
    total = np.append(total, end)

    return expit(total)


def test_sound():
    data = get_sound_data('../sounds/03orangecrush.wav')
    save_wav(data, 'test.wav')

if __name__ == "__main__":
    test_sound()