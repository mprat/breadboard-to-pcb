import Image
import sys
import ImageFilter
import numpy as np
import ImageTk
import Tkinter as tk
from wire import Wire

arr = []
wires = [] #array of Wire objects
colorthresh = 10
recursiondepth = 10
im = []
root = tk.Tk()

def wait():
	raw_input("Press enter to continue")

def showImg(image, show):
	if (show == "show"):
		image.show()

#metric of how close two rgb values are 
# (just use euclidean distance for now)
def closeRGB(rgb1, rgb2):
	return np.linalg.norm(rgb1 - rgb2)

def makeWire(wire, firstpt):
	wire.addPixelLoc(makeWireHelper(firstpt, recursiondepth))

def makeWireHelper(pt, recurdepth):
	toreturn = set([pt])
	if recurdepth > 0:
		#check all pixels around the pt
		#the index in positions is the "telephone keypad 
		#positions" of each of the positions
		positions = set()
		positions.add((pt[0] - 1, pt[1] - 1))
		positions.add((pt[0] - 1, pt[1]))
		positions.add((pt[0] - 1, pt[1] + 1))
		positions.add((pt[0], pt[1] - 1))
		positions.add((pt[0], pt[1] + 1))
		positions.add((pt[0] + 1, pt[1] - 1))
		positions.add((pt[0] + 1, pt[1]))
		positions.add((pt[0] + 1, pt[1] + 1))
		for p in positions:
			#print closeRGB(arr[pt[0], pt[1]], arr[p[0], p[1]])
			if closeRGB(arr[pt[0], pt[1]], arr[p[0], p[1]]) < colorthresh:
				if p not in toreturn:
					toreturn.add(p)
					toreturn.update(makeWireHelper(p, recurdepth - 1))
	return toreturn	

def seeWire(wire, frame):
	for w in wire.getPixelLoc:
		im.putpixel(w, [255, 255, 255])
	frameimage = ImageTk.PhotoImage(im)
	frame.image = frameimage

def callback(event):
	#print "click at ", event.x, event.y
	#print arr[event.y, event.x]
	wires.append(Wire())
	#wires[-1].addPixelLoc([event.y, event.x])
	makeWire(wires[-1], (event.y, event.x))
	print wires[-1]
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
	panel1.image = frameimage	

	root.mainloop()	
