import Image
import sys
import numpy as np
import ImageTk
import Tkinter as tk
from component import Component
import segmentation as seg

################### GLOBAL VARS #################
arr = []
components = [] #array of component objects
colorthresh = 25
im = []
root = tk.Tk()
panel1 = []


################# UTILITY METHODS ##################

def wait():
	raw_input("Press enter to continue")

def showImg(image, show):
	if (show == "show"):
		im = ImageTk.PhotoImage(image)
		local = tk.Toplevel(master=root)
		panel1 = tk.Label(local, image=im)
		panel1.image = im
		panel1.pack(side="top", fill="both", expand="yes")


################# CATHERIO HAS NO IDEA WHAT THESE DO ##################

def getColor(pt):
	return arr[pt[0], pt[1]]

def makeComponent(comp, firstpt):
	ptstocheck = set([firstpt])
	checked = set()

	#need to seed the wire with the first color
	comp.addPixelLoc(firstpt, getColor(firstpt))	

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

def check_breaks():
	return False

def checkNeighbors(pt, checkedpts, comp):
	toreturn = set()
#	positions = getValidNeighbors(pt)
	positions = comp.getValidNeighbors(pt)
	for p in positions:
		if comp.closeRGB(getColor(p)) < colorthresh:
			comp.addPixelLoc(p, getColor(p))
			if p not in checkedpts:
				toreturn.add(p)
	return toreturn

def seeComponent(comp):
	newim = im.copy()
	for c in comp.getPixelLoc():
		newim.putpixel((c[1], c[0]), (255, 255, 255))
	for c in comp.getBoundary():
		newim.putpixel((c[1], c[0]), (255, 0, 0))
	panel1.image = ImageTk.PhotoImage(newim)
	newim.show()

def makeComponentCallback(event):
	print "click at ", event.x, event.y, " . Please wait."
	#print arr[event.y, event.x]
	components.append(Component(arr.shape[0], arr.shape[1]))
	#wires[-1].addPixelLoc([event.y, event.x])
	makeComponent(components[-1], (event.y, event.x))
	seeComponent(components[-1])	
	print "End click. Ready to process another"

def showClickCallback(event):
	print "click at", event.x, event.y, ". Doing nothing about it."

################ MAIN EVENT LOOP ####################
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
	panel1.bind("<Button-1>", showClickCallback)

	root.mainloop()	
