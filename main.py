import Image
import sys
import ImageFilter
import numpy as np
import ImageTk
import Tkinter as tk

def wait():
	raw_input("Press enter to continue")

def showImg(image, show):
	if (show == "show"):
		image.show()

def callback(event):
	print "click at ", event.x, event.y

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
