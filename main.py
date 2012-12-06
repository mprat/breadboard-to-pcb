import Image
import sys
import getopt
import numpy as np
import ImageTk
import Tkinter as tk
from component import Component
import segmentation as seg

################### GLOBAL VARS #################
root = tk.Tk()
colorthresh = 25
show = True

arr = []
components = [] #array of component objects
im = []
panel1 = []

################# UTILITY METHODS ##################

def wait():
    raw_input("Press enter to continue")

def showImg(image):
    if show:
        im = ImageTk.PhotoImage(image)
        local = tk.Toplevel(master=root)
        panel = tk.Label(local, image=im)
        panel.image = im
        panel.pack(side="top", fill="both", expand="yes")


################# COMPONENT-FINDING METHODS ##################

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
#    positions = getValidNeighbors(pt)
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
    showImg(newim)


################ MAIN WINDOW CLICK CALLBACKS ####################

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

def main():
    """Main loop.
    First argument should be a filename
    Second argument should be 'show' or other, to show or not show images
    """
    try:
	opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
	print msg
	print "for help use --help"
	sys.exit(2)
    for o, a in opts:
	if o in ("-h", "--help"):
	    print main.__doc__
	    sys.exit(0)
    if (len(args) != 2):
	print "Incorrect command line arguments. For help use --help"
	sys.exit(0)
    else:
        # Set configuration
        showstr = sys.argv[2]
        global show
       	show = (showstr == 'show')

        # Load the image
        filename = sys.argv[1]
        global im
        im = Image.open("imgs/"+ filename) # global
        global arr
        arr = np.array(im) # global; r = arr[:, :, 0] etc.
        showImg(im)
        print im.format, im.size, im.mode 
        
        # Set up main panel with appropriate callback
        frameimage = ImageTk.PhotoImage(im)
        panel1 = tk.Label(root, image=frameimage)
        panel1.pack(side="top", fill="both", expand="yes")
        panel1.bind("<Button-1>", showClickCallback)

        # Do modesegmentation, show
        imsegmode = seg.modeSegment(im)
        showImg(imsegmode)
        
        root.mainloop()

if __name__ == "__main__":
    main()
