
# Weaving Beats

import numpy as np
from sound_functions import get_sound_data, save_wav, envelope


# settings for the fractal:
recursion_depth = 4
seconds = 20
songfile = '../sounds/testsounds/found.wav'
outputfile = 'weaving.wav'


# These transformations define the fractal.
# The first two numbers are the start/end location of the space transformation
# The third is the multiplier for the note which determines the location
# from which the sample is drawn. 
transformations = [
	[0, 0.25, 4],
	[0.5, 0, 3],
	[0.75, 0.25, 7],
	[0.5, 1, 2]
]



def main():


	basesong = get_sound_data(songfile)

	rate = 44100
	newsong = np.zeros(seconds*rate,dtype=np.float32)
	loc = newsong.shape[0]/2.0


	weaving_beats(basesong, newsong, recursion_depth, 0, newsong.shape[0], 1)
	save_wav(newsong, outputfile)



def weaving_beats(song, outsong, depth, start, end, note):
	width = int(end) - int(start)
	if end >= outsong.shape[0] + width:
		end = end % outsong.shape[0]
	if(start < 0):
		start = start + outsong.shape[0]


	if depth <= 0:

		clipstart = note*abs(width)
		usewidth = abs(width) #min(abs(width), 50000) # uncomment to create a clipped effect
		clipend = clipstart + usewidth
		while (clipend >= song.shape[0]):

			clipstart= clipend % song.shape[0]
			clipend = clipstart +  usewidth


		clip = song[clipstart:clipend]

		cliplen = int(clip.shape[0])
		env = 	envelope(cliplen, 500, 1000)

		if(start + usewidth >= outsong.shape[0]):
			usewidth = outsong.shape[0] - start 

		outsong[int(start):int(start) + usewidth] += 0.08*clip[0:usewidth]*envelope(usewidth, 500, 1000)

		return

	for t in transformations:
		

		weaving_beats(song, outsong, depth - 1, start + width*t[0], start + width*t[1], note*t[2])


if __name__ == "__main__":
	main()