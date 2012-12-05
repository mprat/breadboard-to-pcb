import numpy as np

class Wire:
	def __init__(self):
		self.pixelLoc = []
		self.RGBcolors = []

	def addPixelLoc(self, pixelloc, rgbcolor):
		self.pixelLoc.extend(pixelloc)
		self.RGBcolors.extend(rgbcolor)

	def __str__(self):
		return self.pixelLoc.__str__()

	def getPixelLoc(self):
		return self.pixelLoc

	def getRGBavg(self):
		#axis=0 means the rgb-triple is the thing being averaged
		if (len(self.RGBcolors) < 1):
			print "Error. Should never get here"
			sys.exit(1)
		else:
			return np.average(self.RGBcolors, axis=0)
