import numpy as np
import wire as w

def addPixelLoc(newpixelloc, newrgbcolor, pixelLocations, RGBcolors, boundarypixels):
	pixelLocations.append(newpixelloc)
	RGBcolors.append(newrgbcolor)
	if (len(boundarypixels) < 1):
		boundarypixels.add(newpixelloc)
	else:
		updateNeighbors(newpixelloc, boundarypixels) #TOFIX

def updateNeighbors(newpixelloc, pixelLocations, boundarypixels, img_width, img_height):
	neighborstoupdate = [newpixelloc]

	while (len(neighborstoupdate) > 0):
		neighbortoupdate = neighborstoupdate.pop()
		if isBoundary(neighbortoupdate, pixelLocations, boundarypixels, img_width, img_height):
			boundarypixels.add(neighbortoupdate)
			for n in neighborsInComp(neighbortoupdate, pixelLocations, img_width, img_height):
				if not isBoundary(n, pixelLocations, boundarypixels, img_width, img_height) and n in boundarypixels:
					boundarypixels.remove(n)
					neighborstoupdate.extend(neighborsInComp(n, pixelLocations, img_width, img_height))

def isBoundary(newpixelloc, pixelLocations, boundarypixels, img_width, img_height):
	if 8 - len(neighborsInComp(newpixelloc, pixelLocations, img_width, img_height)) >= 3:
		boundarypixels.add(newpixelloc)
		return True

def neighborsInComp(newpixelloc, pixelLocations, img_width, img_height):
	#use set intersection for faster performance
	return [i for i in getValidNeighbors(newpixelloc, img_width, img_height) if i in pixelLocations]

def getRGBavg(RGBcolors):
	#axis=0 means the rgb-triple is the thing being averaged
	if (len(RGBcolors) < 1):
		print "Error. Should never get here"
		sys.exit(1)
	else:
		return np.average(RGBcolors, axis=0)

def getRGBavgastuple(RGBcolors):
	return tuple(map(int, getRGBavg(RGBcolors)))

def closeRGB(rgb, RGBavg):
	return np.linalg.norm(RGBavg - rgb)

#img_height = number of rows = arr.shape[0]
#img_width = number of cols = arr.shape[1]
def getValidNeighbors(pt, img_width, img_height, nsew_only=False):
	positions = set()
	
	# add the next points to check onto the queue in a smart way
	# wires are more likely to go up-down or side-side, so check 
	# positions 2, 6, 8, and 4 last (so that they get popped first)
	if not nsew_only:
		if (pt[0] - 1 > 0) and (pt[1] - 1 > 0):
			positions.add((pt[0] - 1, pt[1] - 1)) #1
		if (pt[1] + 1 < img_width) and (pt[0] + 1 < img_height): #x-value can't be greater than the number of rows
			positions.add((pt[0] + 1, pt[1] + 1)) #9
		if (pt[0] - 1 > 0) and (pt[1] + 1 < img_width): #y-value can't be greater than the number of cols
			positions.add((pt[0] - 1, pt[1] + 1)) #3
		if (pt[1] - 1 > 0) and (pt[0] + 1 < img_height):
			positions.add((pt[0] + 1, pt[1] - 1)) #7
	if (pt[0] - 1 > 0):
		positions.add((pt[0] - 1, pt[1])) #2
	if pt[1] - 1 > 0:
		positions.add((pt[0], pt[1] - 1)) #4
	if pt[1] + 1 < img_width:
		positions.add((pt[0], pt[1] + 1)) #6
	if pt[0] + 1 < img_height:
		positions.add((pt[0] + 1, pt[1])) #8
	return positions

def getLeftMostPixel(pixels):
	return min(pixels, key=lambda x:x[0])

def getRightMostPixel(pixels):
	return max(pixels, key=lambda x:x[0])

def getTopMostPixel(pixels):
	return max(pixels, key=lambda x:x[1])

def getBottomMostPixel(pixels):
	return min(pixels, key=lambda x:x[1])

def makeWire(pixels):
	left = getLeftMostPixel(pixels)
	right = getRightMostPixel(pixels)
	top = getTopMostPixel(pixels)
	bottom = getBottomMostPixel(pixels)
	if (np.linalg.norm(left - right) < 2):
		return w.Wire(top[0], top[1], bottom[0], bottom[1])
	elif (np.linalg.norm(top - bottom) < 2):
		return w.Wire(left[0], left[1], right[0], right[1])
