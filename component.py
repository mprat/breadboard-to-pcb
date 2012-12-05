import numpy as np

class Component:
	def __init__(self, imgheight, imgwidth):
		self.pixelLoc = []
		self.RGBcolors = []
		self.boundarypixels = []
		self.img_width = imgwidth
		self.img_height = imgheight

	def addPixelLoc(self, pixelloc, rgbcolor):
		self.pixelLoc.append(pixelloc)
		self.RGBcolors.append(rgbcolor)
		if (len(self.boundarypixels) < 1):
			self.boundarypixels.append(pixelloc)
		else:
			neighbors = self.getValidNeighbors(pixelloc[0])
			count_n = 0
			for n in neighbors:
				if n not in self.pixelloc:
					count_n += 1
			print "count_n = ", count_n

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

	#img_height = number of rows = arr.shape[0]
	#img_width = number of cols = arr.shape[1]
	def getValidNeighbors(self, pt, nsew_only=False):
		positions = set()
		
		# add the next points to check onto the queue in a smart way
		# wires are more likely to go up-down or side-side, so check 
		# positions 2, 6, 8, and 4 last (so that they get popped first)
		if not nsew_only:
			if (pt[0] - 1 > 0) and (pt[1] - 1 > 0):
				positions.add((pt[0] - 1, pt[1] - 1)) #1
			if (pt[1] + 1 < self.img_width) and (pt[0] + 1 < self.img_height): #x-value can't be greater than the number of rows
				positions.add((pt[0] + 1, pt[1] + 1)) #9
			if (pt[0] - 1 > 0) and (pt[1] + 1 < self.img_width): #y-value can't be greater than the number of cols
				positions.add((pt[0] - 1, pt[1] + 1)) #3
			if (pt[1] - 1 > 0) and (pt[0] + 1 < self.img_height):
				positions.add((pt[0] + 1, pt[1] - 1)) #7
		if (pt[0] - 1 > 0):
			positions.add((pt[0] - 1, pt[1])) #2
		if pt[1] - 1 > 0:
			positions.add((pt[0], pt[1] - 1)) #4
		if pt[1] + 1 < self.img_width:
			positions.add((pt[0], pt[1] + 1)) #6
		if pt[0] + 1 < self.img_height:
			positions.add((pt[0] + 1, pt[1])) #8
		return positions

