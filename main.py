import Image
import sys
import ImageFilter
import numpy as np
import ImageTk
import Tkinter as tk
from wire import Wire

arr = [];
wire1 = Wire()

def wait():
	raw_input("Press enter to continue")

def showImg(image, show):
	if (show == "show"):
		image.show()

#metric of how close two rgb values are 
# (just use euclidean distance for now)
def closeRGB(rgb1, rgb2):
	return np.linalg.norm(rgb1 - rgb2)

def callback(event):
	print "click at ", event.x, event.y
	print arr[event.y, event.x]
	wire1.addPixelLoc([event.y, event.x])
	print wire1	
	
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
	print arr[0, 0] #each pixel

	#tkinter to get user click from the screen
	root = tk.Tk()
	frameimage = ImageTk.PhotoImage(im)
	panel1 = tk.Label(root, image=frameimage)
	panel1.pack(side="top", fill="both", expand="yes")
	panel1.bind("<Button-1>", callback)
	panel1.image = frameimage	

	root.mainloop()	
