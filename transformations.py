
# Edit here to vary the fractal.
# initialize values for time1, time2, freq1, freq2, amp1, amp2
# these are initial lines in three interlocking 1-d IFS's. values should be 0-1
#


geometric_clouds = [
	[0, 0.5, 0.25, 1, 0, 0.75],
	[0.75, 0.5, 0.75, 0.5, 0.5, 0],
	[0.5, 1, 0, 0.25, 0.25, 0.75],
	[0.75, 1, 0.75, 1, 1, 0.75]
]

def current_transformation():
	return geometric_clouds
