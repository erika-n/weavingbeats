
# Weaving Beats

import numpy as np
import wave
import scipy.io.wavfile as wav
from sound_functions import envelope
import getopt, sys




# These transformations define the fractal. See https://en.wikipedia.org/wiki/Barnsley_fern


# transformations = [
#	[0, 0, 0.16, 0, 0, 0.01],
#	[0.85, 0.04, -0.04, 0.85, 0, 1.60, 0.85],
#	[0.20, -0.26, 0.23, 0.22, 0, 1.60, 0.07],
#	[-0.15, 0.28, 0.26, 0.24, 0, 0..44, 0.07]
# ]

transformations = [
	[0.25, 0, 0.5, -0.25, 0.5, 0, 0.01],
	[0.5, 0.75, 0.5, 0, 0, 0.5, 0.85]
	# [1, -0.5, 0, 0.5, 0.5, 0, 0.07],
	# [-0.25, 0, 0, 1, 0, 0, 0.07]
]


copysamples = 2000

def  fern_music(songfile, outputfile, seconds, depth):

	print "fern_musics"
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

	r_fern_music(depth, x, y, transformations, newsong, basesong)


	data = newsong.astype(np.int16)
	print "data = " + str(data.size)
	z = np.zeros(data.shape, dtype=np.int16)
	data = np.append(data, z)
	print "writing " + str(data.size) + " samples"
	output_file = wave.open(outputfile, "w")
	output_file.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
	output_file.writeframes(data)
	output_file.close()




def r_fern_music(depth, x, y, transformations, newsong, basesong):
	if(depth <= 0):
		

		new_loc = int(newsong.size*y)
		old_loc = int(basesong.size*x)
		amp = 0.01
		c = copysamples
		if(c + old_loc < basesong.size - 1 and c + new_loc < newsong.size -1  and old_loc > c and new_loc > c):
			print "."
			newsong[new_loc - c:new_loc+ c] += amp*basesong[old_loc - c:old_loc+c] 
		return

	ts = np.array(transformations)
	probs = ts[:, 6]


	
	for i in range(len(transformations)):
		t = transformations[i]
		nx = t[0]*x + t[1]*y + t[4]
		ny = t[2]*x + t[3]*y + t[5]	
		r_fern_music(depth - 1, nx, ny, transformations, newsong, basesong)
 


if __name__ == "__main__":


	argv = sys.argv[1:]
	inputfile = ''
	outputfile = ''
	seconds = 10
	depth = 2
	try:
		opts, args = getopt.getopt(argv,"o:i:s:d:",["ofile=", "ifile=", "seconds=", "iters="])
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
		elif opt in ("-d", "--depth"):
			depth = int(arg)

	fern_music(inputfile, outputfile, seconds, depth)