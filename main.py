import Image
import sys
import numpy as np
import ImageTk
import Tkinter as tk
from component import Component
import segmentation as seg

arr = []
components = [] #array of component objects
colorthresh = 25
im = []
root = tk.Tk()
panel1 = []

def wait():
	raw_input("Press enter to continue")

def showImg(image, show):
	if (show == "show"):
		image.show()

def getColor(pt):
	return arr[pt[0], pt[1]]

def makeComponent(comp, firstpt):
	ptstocheck = set([firstpt])
	checked = set()

	#need to seed the wire with the first color
	comp.addPixelLoc([firstpt], getColor(firstpt))	

	loopcounter = 0
	while len(ptstocheck) > 0:
		loopcounter += 1
		pt = ptstocheck.pop()
		if pt not in checked:
			checked.add(pt)
			ptsfromneighbor = checkNeighbors(pt, checked, comp)
			ptstocheck.update(ptsfromneighbor)
		if loopcounter > 1000:
			print "Probably detecting a component incorrectly!"
			break

def checkNeighbors(pt, checkedpts, comp):
	toreturn = set()
	positions = set()
	
	# add the next points to check onto the queue in a smart way
	# wires are more likely to go up-down or side-side, so check 
	# positions 2, 6, 8, and 4 last (so that they get popped first)
	
	if (pt[0] - 1 > 0) and (pt[1] - 1 > 0):
		positions.add((pt[0] - 1, pt[1] - 1)) #1
	if (pt[1] + 1 < arr.shape[1]) and (pt[0] + 1 < arr.shape[0]): #x-value can't be greater than the number of rows
		positions.add((pt[0] + 1, pt[1] + 1)) #9
	if (pt[0] - 1 > 0) and (pt[1] + 1 < arr.shape[1]): #y-value can't be greater than the number of cols
		positions.add((pt[0] - 1, pt[1] + 1)) #3
	if (pt[1] - 1 > 0) and (pt[0] + 1 < arr.shape[0]):
		positions.add((pt[0] + 1, pt[1] - 1)) #7
	if (pt[0] - 1 > 0):
		positions.add((pt[0] - 1, pt[1])) #2
	if pt[1] - 1 > 0:
		positions.add((pt[0], pt[1] - 1)) #4
	if pt[1] + 1 < arr.shape[1]:
		positions.add((pt[0], pt[1] + 1)) #6
	if pt[0] + 1 < arr.shape[0]:
		positions.add((pt[0] + 1, pt[1])) #8

	for p in positions:
		if comp.closeRGB(getColor(p)) < colorthresh:
			comp.addPixelLoc([p], getColor(p))
			if p not in checkedpts:
				toreturn.add(p)
	return toreturn

def seeComponent(comp):
	newim = im.copy()
	for c in comp.getPixelLoc():
		newim.putpixel((c[0][1], c[0][0]), (255, 255, 255))
	panel1.image = ImageTk.PhotoImage(newim)
	newim.show()

def callback(event):
	print "click at ", event.x, event.y, " . Please wait."
	#print arr[event.y, event.x]
	components.append(Component())
	#wires[-1].addPixelLoc([event.y, event.x])
	makeComponent(components[-1], (event.y, event.x))
	seeComponent(components[-1])	
	print "End click. Ready to process another"
	
# write name of file in command-line arguments
if (len(sys.argv) != 3):
	sys.exit(0)
else:
	filename = sys.argv[1]
	showstr = sys.argv[2]	

	im = Image.open("imgs/"+ filename)
	showImg(im, showstr)
	
	imsegmode = seg.modeSegment(im)
	showImg(imsegmode, showstr)

	#doublecheck format, size, and mode
	print im.format, im.size, im.mode 
	
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
