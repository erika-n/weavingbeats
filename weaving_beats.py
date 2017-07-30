
# Weaving Beats
# Erika Nesse, 2016. 

import numpy as np
from sound_functions import get_sound_data, save_wav, envelope
from transformations import current_transformation
import argparse


# the fractal itself is defined in transformations.py
transformations = current_transformation()

def main():


	basesong = get_sound_data(inputfile)

	rate = 44100

	newsong = np.zeros(seconds*rate,dtype=np.float32)
	loc = newsong.shape[0]/2.0


	weaving_beats(basesong, newsong, recursion_depth, 0, 1, 0, 1, 0, 1)
	newsong *= 0.5*(1.0/np.max(newsong)) #correct amplitude
	save_wav(newsong, outputfilename + ".wav")



def weaving_beats(song, outsong, depth, time1, time2, freq1, freq2, amp1, amp2):
	twidth = time2 - time1
	fwidth = freq2 - freq1
	awidth = amp2 - amp1



	if depth <= 0:

		#get clip by applying 
		freq = (freq2 - freq1)/2
		clipwidth = int(twidth*outsong.shape[0]) 
		clipstart  =int(freq*song.shape[0])
		clipend = clipstart + clipwidth
		clip = song.take(range(clipstart, clipend), mode='wrap');


		amp = (amp2 - amp1)/2

		outstart = int(time1*outsong.shape[0])
		outend = outstart + clipwidth
		if(outend > outsong.shape[0]):
			outend = -1*(outend % outsong.shape[0])

		env = envelope(clipwidth, 30, 30)
		outsong[outstart:outend] += amp*clip[:]*env
		return

	for t in transformations:

		# apply transformation: shrink each line and move it according to the transformation, for time, frequency, and amplitude
		weaving_beats(song, outsong, depth - 1, time1 + twidth*t[0], time1 + twidth*t[1], freq1 + fwidth*t[2], freq1 + fwidth*t[3], amp1 + awidth*t[4], amp1 + awidth*t[5])


if __name__ == "__main__":




	parser = argparse.ArgumentParser(description='Make a fractal from a sound file.')

	parser.add_argument('-s', '--seconds',default=20,
	                    help='seconds of music', type=int)
	parser.add_argument('-i', '--inputfile' ,
	                    help='input file (.wav)')
	parser.add_argument('-o', '--outputfilename' , default = 'fractal',
	                    help="output filename (don't add extension")
	parser.add_argument('-d', '--depth' , default = 3, type=int,
	           
	                    help='fractal recursion depth (level of detail)')



	args = parser.parse_args()
	seconds = args.seconds
	
	inputfile = args.inputfile
	outputfilename = args.outputfilename
	recursion_depth = args.depth
	main()
