import Image
import sys
import ImageFilter
import numpy as np
import ImageTk
import Tkinter as tk
from wire import Wire

arr = []
wires = [] #array of Wire objects
colorthresh = 12
im = []
root = tk.Tk()
panel1 = []
temppts = set()

def wait():
	raw_input("Press enter to continue")

def showImg(image, show):
	if (show == "show"):
		image.show()

#metric of how close two rgb values are 
# (just use euclidean distance for now)
def closeRGB(rgb1, rgb2):
	return np.linalg.norm(rgb1 - rgb2)

def getColor(pt):
	return arr[pt[0], pt[1]]

def makeWire(wire, firstpt):
	ptstocheck = set([firstpt])
	checked = set()
	wirepts = set([firstpt])

	#need to seed the wire with the first color
	wire.addPixelLoc([firstpt], getColor(firstpt))	

	while len(ptstocheck) > 0:
		pt = ptstocheck.pop()
		if pt not in checked:
			ptsfromneighbor = checkNeighbors(pt, checked, wire)
			#wirepts.update(ptsfromneighbor)
			ptstocheck.update(ptsfromneighbor)
			checked.add(pt)
	#wire.addPixelLoc(wirepts)

def checkNeighbors(pt, checkedpts, wire):
	toreturn = set()
	positions = set()
	
	if pt[0] - 1 > 0:
		positions.add((pt[0] - 1, pt[1])) #2
		if pt[1] - 1 > 0:
			positions.add((pt[0] - 1, pt[1] - 1)) #1
		if pt[1] + 1 < arr.shape[1]: #y-value can't be greater than the number of cols
			positions.add((pt[0] - 1, pt[1] + 1)) #3
	if pt[1] - 1 > 0:
		positions.add((pt[0], pt[1] - 1)) #4
		if pt[0] + 1 < arr.shape[0]: #x-value can't be greater than number of rows
			positions.add((pt[0] + 1, pt[1] - 1)) #7
	if pt[1] + 1 < arr.shape[1]:
		positions.add((pt[0], pt[1] + 1)) #6
		if pt[0] + 1 < arr.shape[0]:
			positions.add((pt[0] + 1, pt[1] + 1)) #9
	if pt[0] + 1 < arr.shape[0]:
		positions.add((pt[0] + 1, pt[1])) #8
	for p in positions:
		if closeRGB(arr[pt[0], pt[1]], arr[p[0], p[1]]) < colorthresh:
			wire.addPixelLoc([p], getColor(p))
			if p not in checkedpts:
				toreturn.add(p)
	return toreturn

def seeWire(wire, frame):
	for w in wire.getPixelLoc():
		im.putpixel((w[1], w[0]), (255, 255, 255))
	panel1.image = ImageTk.PhotoImage(im)
	im.show()

def callback(event):
	#print "click at ", event.x, event.y
	#print arr[event.y, event.x]
	wires.append(Wire())
	#wires[-1].addPixelLoc([event.y, event.x])
	makeWire(wires[-1], (event.y, event.x))
	seeWire(wires[-1], event.widget)	
	
# write name of file in command-line arguments
if (len(sys.argv) != 3):
	sys.exit(0)
else:
	filename = sys.argv[1]
	showstr = sys.argv[2]	

	im = Image.open("imgs/"+ filename)
	showImg(im, showstr)
	
	#doublecheck format, size, and mode
	print im.format, im.size, im.mode 
	
	#can get an image without the holes in the breadboard from a modefilter
	#the number is hard-coded and made up for now
	immodefilter = im.filter(ImageFilter.ModeFilter(10))
	showImg(immodefilter, showstr)
	
	arr = np.array(im)
	r = arr[:, :, 0]
	g = arr[:, :, 1]
	b = arr[:, :, 2]
	#print arr[0, 0] #each pixel

	#tkinter to get user click from the screen
	frameimage = ImageTk.PhotoImage(im)
	panel1 = tk.Label(root, image=frameimage)
	panel1.pack(side="top", fill="both", expand="yes")
	panel1.bind("<Button-1>", callback)
	#panel1.image = frameimage	

	root.mainloop()	
