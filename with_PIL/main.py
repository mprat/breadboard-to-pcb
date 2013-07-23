import time
import Image
import sys
import getopt
import numpy as np
import ImageTk
import Tkinter as tk
from component import Component
import segmentation as seg
from Tkinter import RIGHT, LEFT, BOTH, RAISED, DISABLED
import ttk
import Queue
import matplotlib.pyplot as plt
import component_utils as cu

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
    (val, i) = min((np.linalg.norm(np.array(x) - np.array(m)),i) for (i,m) in enumerate(options))
    return options[i]

def curry_f(f, second):
    def f_curried(first):
        print first
        return f(first, second)
    return f_curried

def rgbToHex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)

def hexToRgb(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

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
    components[-1].getLeftMostPixel()
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

colorQueue = Queue.Queue()
def queueColorCallback(event):
    print "Enqueueing click at", event.x, event.y, " by color ", arr[event.y, event.x]
    global colorQueue
    colorQueue.put(arr[event.y, event.x]) # intentionally reversed

clickList = list()
def accumulateClicksCallback(event):
    print "Enqueueing click at", event.x, event.y, " by position"
    global clickList
    clickList.append([event.y, event.x]) # intentionally reversed

################ COLOR SELECTION GUI ####################

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
                
        numColors = 5
        self.colorButton = list()
        for i in range(numColors):
            self.colorButton.append(tk.Button(self, text="Color " + str(i), foreground="#000000", background="#FFFFFF", command = (lambda x: lambda: changeButtonColor(self, x))(i)))
            self.colorButton[i].pack(side=LEFT, padx=5, pady=5)
        
        self.okButton = tk.Button(self, text="OK", command = (lambda: confirmColors(self)))
        self.okButton.pack(side=RIGHT, padx=5, pady=5)
        
        frameimage = ImageTk.PhotoImage(im, master=root)
        self.panel1 = tk.Label(frame, image=frameimage)
        self.panel1.image = frameimage
        self.panel1.pack(side="top", fill="both", expand="yes")

        self.panel1.bind("<Button-1>", queueColorCallback)
        self.panel1.pack(side=LEFT, padx=5, pady=5)

def changeButtonColor(frame, i):
    button = frame.colorButton[i]
    global colorQueue
    try:
        color = colorQueue.get_nowait()
        print "Got color", color
        button["bg"] = rgbToHex(color)
    except:
        print "Incorrect use; click on a pixel first"

def confirmColors(frame):
    for button in frame.colorButton:
        button["state"] = DISABLED

    # Do the transformation
    palette = [hexToRgb(button["bg"]) for button in frame.colorButton]
    print "Transforming palette"
    b = seg.paletteTransformIm(im, palette) # TODO: not im, use more generalized
    print "Finding connected components"
    (c,n) = seg.connectedComponents(np.array(b), palette)
    frame.labels = c
    frame.nlabels = n
    
    # Set up new GUI appearance/functionality
    print "Displaying result"
    c_im = Image.fromarray(c)
    toshow = ImageTk.PhotoImage(c_im, master=root)
    frame.panel1["image"] = toshow
    frame.panel1.image = toshow
    frame.panel1.bind("<Button-1>", accumulateClicksCallback)
    frame.okButton["command"] = (lambda: processClickList(frame))
    print "Done"

def processClickList(frame):
    print "Processing click list!"
    comps = list()
    for click in clickList:
        mask = (frame.labels == frame.labels[click[0], click[1]])
        comps.append(Component(mask))
    showComps(comps)
    wires = list()
    for c in comps:
        wires.append(cu.makeWire(c.getPixels()))
    makeSchematic(wires, str(int(time.time())) + '_schematic')

def showComps(comps):
    for c in comps:
        mask = c.getMask()
        i = Image.fromarray(mask)
        i.mode = '1'
        showBinaryImg(i)
        # toshow = ImageTk.PhotoImage(i, master=root)

def makeSchematic(wires, filename):
    cu.makeXMLFile(wires, filename)
    print "Done writing to file"

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
