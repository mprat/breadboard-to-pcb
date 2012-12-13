import numpy as np

class Component:
	def __init__(self, mask):
		self.mask = mask
		print self.mask.shape
	
	def getPixels(self):
		pixels = []
		for i in range(self.mask.shape[0]):
			for j in range(self.mask.shape[1]):
				if (self.mask[i][j] == 1):
					pixels.append((i, j))
		return np.array(pixels)

	def getMask(self):
		return self.mask
