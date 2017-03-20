
# Weaving Beats

import numpy as np
import wave
import scipy.io.wavfile as wav
from sound_functions import envelope
import getopt, sys

# settings for the fractal:
recursion_depth = 6
seconds = 120


# These transformations define the fractal. See https://en.wikipedia.org/wiki/Barnsley_fern


# transformations = [
#	[0, 0, 0.16, 0, 0, 0.01],
#	[0.85, 0.04, -0.04, 0.85, 0, 1.60, 0.85],
#	[0.20, -0.26, 0.23, 0.22, 0, 1.60, 0.07],
#	[-0.15, 0.28, 0.26, 0.24, 0, 0..44, 0.07]
# ]

transformations = [
	[0, 0, 0.0, 0.16, 0, 0, 0.01],
	[0.85, 0.04, -0.04, 0.85, 0, 1.60, 0.85],
	[0.20, -0.26, 0.23, 0.22, 0, 1.60, 0.07],
	[-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07]
]


copysamples = 1


def  fern_music(songfile, outputfile, seconds, iters):

    data = wav.read(songfile)
    rate = data[0]
    data = data[1]/2
    data = data.astype(np.float32)
   
  
    # Convert to mono

    if(data.ndim > 1):
        data = np.sum(data, axis=1)

	basesong = data
	newsong = np.zeros((rate*seconds), dtype=np.float32)
	print "rate = " + str(rate)
	print "seconds = " + str(seconds)
	print "newsong = " + str(newsong.size)
	x = 0.01
	y = 0.01
	ts = np.array(transformations)
	probs = ts[:, 6]

	amp = 0.1
	env = amp*envelope(copysamples, copysamples/3, copysamples/3)

	for i in range(iters):
		if(i % 10000 == 0):
			print "i = " + str(i)
		c = np.random.choice(probs.size, p=probs)
		t = transformations[c]
		x = t[0]*x + t[1]*y + t[4]
		y = t[2]*x + t[3]*y + t[5]
		new_loc = int(newsong.size*y/9.999)
		old_loc = int(basesong.size*(x + 2.182))/(2.182 + 2.6558)
	
		
		if(copysamples + old_loc < basesong.size - 1 and copysamples+ new_loc < newsong.size -1 ):

			#print "copying..."
	
			newsong[new_loc:new_loc + copysamples] += amp*basesong[old_loc:old_loc+copysamples] 

	

	data = newsong.astype(np.int16)
	print "data = " + str(data.size)
	z = np.zeros(data.shape, dtype=np.int16)
	data = np.append(data, z)
	print "writing " + str(data.size) + " samples"
	output_file = wave.open(outputfile, "w")
	output_file.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
	output_file.writeframes(data)
	output_file.close()





if __name__ == "__main__":


	argv = sys.argv[1:]
	inputfile = ''
	outputfile = ''
	seconds = 10
	iters = 2000
	try:
		opts, args = getopt.getopt(argv,"o:i:s:r:",["ofile=", "ifile=", "seconds=", "iters="])
	except getopt.GetoptError:
		print 'fractal_fern.py -i <inputfile> -o <outputfile> -s <seconds>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'fractal_fern.py -i <inputfile> -o <outputfile> -s <seconds>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-s", "--seconds"):
			seconds = int(arg)
		elif opt in ("-r", "--iters"):
			iters = int(arg)

	fern_music(inputfile, outputfile, seconds, iters)