import Image
import sys
import getopt
import numpy as np
import ImageTk
import Tkinter as tk
from component import Component
import segmentation as seg
from Tkinter import RIGHT, LEFT, BOTH, RAISED
import ttk
import Queue

################### GLOBAL VARS #################
root = tk.Tk()
colorthresh = 25
show = True

arr = []
components = [] #array of component objects
im = []

################# UTILITY METHODS ##################

def wait():
    raw_input("Press enter to continue")

def showImg(img): # for arrays, instead use pl.imshow
    if show:
        im2 = ImageTk.PhotoImage(img, master=root)
        local = tk.Toplevel(master=root)
        panel = tk.Label(local, image=im2)
        panel.image = im2
        panel.pack(side="top", fill="both", expand="yes")

def showBinaryImg(img):
    assert img.mode == '1'
    if show:
        im2 = ImageTk.BitmapImage(img, master=root)
        local = tk.Toplevel(master=root)
        panel = tk.Label(local, image=im2)
        panel.image = im2
        panel.pack(side="top", fill="both", expand="yes")

def pixelwiseIm(im, transform, mode='RGB'):
# the 'transform' function takes in pixel values and outputs other pixel values
    imPix = im.load()
    out = Image.new(mode, im.size)
    outPix = out.load()
    for x in range(out.size[0]):
        for y in range(out.size[1]):
            newColor = transform(imPix[x, y])
            outPix[x, y] = newColor
    return out

def pixelwiseArr(arr, transform):
# there must be a better way, but I don't know what it is
    out = np.zeros(arr.shape)
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            out[x,y] = transform(arr[x,y])
    return out

def downsample(imArray, byFactor):
    return imArray[range(0, imArray.shape[0], byFactor)][:, range(0, imArray.shape[1], byFactor)]

def closest(x, options):
    (val, i) = min((np.linalg.norm(x - m),i) for (i,m) in enumerate(options))
    return options[i]

def curry_f(f, second):
    def f_curried(first):
        print first
        return f(first, second)
    return f_curried

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
            print "Breaking after 1000 iterations, probably detecting a component incorrectly!"
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

def segmentationCallback(event):
    print "Running full segmentation; ignoring click location and doing something unrelated"
    com = seg.getCOM(im)
    for (size, c) in com:
        print "Finding component at", int(c[0]), int(c[1])
        components.append(Component(arr.shape[0], arr.shape[1]))
        makeComponent(components[-1], (int(c[0]), int(c[1])))
        seeComponent(components[-1])    
    print "Done"

def showClickCallback(event):
    print "Click at", event.x, event.y, " with color ", arr[event.y, event.x]

################ COLOR SELECTION GUI ####################

colorQueue = Queue.Queue()

def queueColorCallback(event):
    print "Enqueueing click at", event.x, event.y, " with color ", arr[event.y, event.x]
    global colorQueue
    colorQueue.put(arr[event.y, event.x])

class ColorSelect(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)            
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.parent.title("Buttons")
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        frame = ttk.Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=1)
        
        self.pack(fill=BOTH, expand=1)
        
        closeButton = tk.Button(self, text="Close")
        closeButton.pack(side=RIGHT, padx=5, pady=5)
                
        numColors = 5
        self.colorButton = list()
        for i in range(numColors):
            self.colorButton.append(tk.Button(self, text="Color " + str(i), foreground="black", background="white", command = (lambda x: lambda: changeButtonColor(self, x))(i)))
            self.colorButton[i].pack(side=LEFT, padx=5, pady=5)
        
        okButton = tk.Button(self, text="OK")
        okButton.pack(side=RIGHT, padx=5, pady=5)
        
        frameimage = ImageTk.PhotoImage(im, master=root)
        panel1 = tk.Label(frame, image=frameimage)
        panel1.image = frameimage
        panel1.pack(side="top", fill="both", expand="yes")

        # # panel1.bind("<Button-1>", makeComponentCallback)
        panel1.bind("<Button-1>", queueColorCallback)
        panel1.pack(side=LEFT, padx=5, pady=5)

def changeButtonColor(frame, i):
    button = frame.colorButton[i]
    global colorQueue
    try:
        color = colorQueue.get_nowait()
        print "Got color", color
        button["bg"] = "#%02x%02x%02x" % tuple(color)
    except:
        print "Incorrect use; click on a pixel first"

################ MAIN EVENT LOOP ####################

def loadIm(filename):
    global im
    im = Image.open("imgs/"+ filename)
    global arr
    arr = np.array(im) #r = arr[:, :, 0] etc.
    print im.format, im.size, im.mode 
    return im

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
        # Set up configuration
        showstr = sys.argv[2]
        global show
       	show = (showstr == 'show')

        # Load the image
        filename = sys.argv[1]
        im = loadIm(filename)
        
        # Set up main panel with appropriate callback
        # frameimage = ImageTk.PhotoImage(im, master=root)
        # panel1 = tk.Label(root, image=frameimage)
        # panel1.pack(side="top", fill="both", expand="yes")
        # # panel1.bind("<Button-1>", makeComponentCallback)
        # panel1.bind("<Button-1>", segmentationCallback)

#        root.geometry("300x200+300+300")
        app = ColorSelect(root)

        root.mainloop()

if __name__ == "__main__":
    main()
