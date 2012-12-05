import numpy as np

class Wire:
	def __init__(self):
		self.pixelLoc = []
		self.RGBcolors = []

	def addPixelLoc(self, pixelloc, rgbcolor=[255, 255, 255]):
		self.pixelLoc.extend(pixelloc)
		self.RGBcolors.extend(rgbcolor)

	def __str__(self):
		return self.pixelLoc.__str__()

	def getPixelLoc(self):
		return self.pixelLoc

	def getRGBavg(self):
		#axis=0 means the rgb-triple is the thing being averaged
		return np.average(self.RGBcolors, axis=0)
