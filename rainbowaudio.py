#!/usr/bin/python3
from mpmath import *
import numpy as np
import math
from sound_functions import save_wav


ticks=3040
seconds = 1
rate = 44100

base_freq = 1000
soundbuffer = np.zeros(480000)

accume=1.0


for ticks in range(1, soundbuffer.shape[0]):

	uon = exp(pi*j*ticks/4096.0)
	aon = exp(pi*j*sqrt(7)*ticks/4096.0)
	ion=exp(pi*j*(-sqrt(7)-3)*ticks/16384.0)
	cue=exp(1*j)
	if(ticks% 1000 == 0):
		print ticks
	for v in range(1,20):
		cue = ((aon + cue) / (aon - cue))*((cue - ion ) / ( cue + uon))
		accume = (accume) * (aon - cue-(accume))/(ion+accume)
		cue = accume
	tha =  ((atan2(cue.real, cue.imag) - math.pi)/(2.0*math.pi))

	#print cue.real

	soundbuffer [ticks] =  sin(ticks*tha*2.0*math.pi*base_freq/rate)


save_wav(soundbuffer, 'testaudio.wav')
