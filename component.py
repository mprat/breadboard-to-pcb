import numpy as np

class Component:
	def __init__(self):
		self.pixelLoc = []
		self.RGBcolors = []
		self.boundarypixels = []

	def addPixelLoc(self, pixelloc, rgbcolor):
		self.pixelLoc.append(pixelloc)
		self.RGBcolors.append(rgbcolor)
		if (len(self.pixelLoc) < 1):
			self.boundarypixels.append(pixelloc)

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

	def getRGBavgastuple(self):
		return tuple(map(int, self.getRGBavg()))

	def closeRGB(self, rgb):
		return np.linalg.norm(self.getRGBavg() - rgb)

	def getBoundary(self):
		return self.boundarypixels
