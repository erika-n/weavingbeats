

import numpy as np
import wave
import scipy.io.wavfile as wav
from sound_functions import envelope
import getopt, sys


# what shall we do.


outputfile = "try_this.wav"
rate = 44100
seconds = 10


newsong = np.zeros((rate*seconds), dtype=np.float32)


# impulse response ideas...

# impulse happens and then?

#nooscillators

# things literally bouncing off walls...

# impulse changing amplitude and smoothing over time

# define a space, sound bounces around
# bouncing back and forth (perhaps recursive, fractal, sure...)

# bouncing, changing amplitude

# impulse response.............

# do the response to the impulse

# then do it again, to the response

# etc



data = newsong.astype(np.int16)
print "data = " + str(data.size)
z = np.zeros(data.shape, dtype=np.int16)
data = np.append(data, z)
print "writing " + str(data.size) + " samples"
output_file = wave.open(outputfile, "w")
output_file.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
output_file.writeframes(data)
output_file.close()

