import numpy as np

class Component:
	def __init__(self, imgheight, imgwidth):
		self.pixelLoc = []
		self.RGBcolors = []
		self.boundarypixels = set([])
		self.img_width = imgwidth
		self.img_height = imgheight

	def addPixelLoc(self, pixelloc, rgbcolor):
		self.pixelLoc.append(pixelloc)
		self.RGBcolors.append(rgbcolor)
		if (len(self.boundarypixels) < 1):
			self.boundarypixels.add(pixelloc)
		else:
			self.updateNeighbors(pixelloc)

	def updateNeighbors(self, newpixelloc):
		neighborstoupdate = [newpixelloc]

		while (len(neighborstoupdate) > 0):
			neighbortoupdate = neighborstoupdate.pop()
			if self.isBoundary(neighbortoupdate):
				self.boundarypixels.add(neighbortoupdate)
				for n in self.neighborsInComp(neighbortoupdate):
					if not self.isBoundary(n) and n in self.boundarypixels:
						self.boundarypixels.remove(n)
						neighborstoupdate.extend(self.neighborsInComp(n))
	
	def getLeftMostPixel(self):
		return min(self.boundarypixels, key=lambda x:x[0])

	def getRightMostPixel(self):
		return max(self.boundarypixels, key=lambda x:x[0])
	
	def getTopMostPixel(self):
		return max(self.boundarypixels, key=lambda x:x[1])

	def getBottomMostPixel(self):
		return min(self.boundarypixels, key=lambda x:x[1])

	def isBoundary(self, pixelloc):
		#neighbors = self.getValidNeighbors(pixelloc)
		#if sum([n not in self.pixelloc for n in neighbors]) >= 3:
		#	return True
		if 8 - len(self.neighborsInComp(pixelloc)) >= 3:
			self.boundarypixels.add(pixelloc)
			return True
	
	def neighborsInComp(self, pixelloc):
		#use set intersection for faster performance
		return [i for i in self.getValidNeighbors(pixelloc) if i in self.pixelLoc]
	
	def __str__(self):
		print "pixelloc = ", self.pixelLoc.__str__()
		return self.xml

	def getPixelLoc(self):
		return self.pixelLoc

	def getBoundary(self):
		return self.boundarypixels

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

