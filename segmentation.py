import Image
import ImageFilter
import cluster
import numpy as np
import main as m
### import skimage # may be useful later
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def modeFilter(im, thresh):
    immodefilter = im.filter(ImageFilter.ModeFilter(thresh))
    return immodefilter

initBeige = np.array((213, 190, 148))
initRed = np.array((152, 55, 29))
initGreen = np.array((37, 55, 39))
initBlack = np.array((43, 42, 47))
initSilver = np.array((130, 129, 125))
initOrange = np.array((126, 69, 50))
allColors = [initBeige, initRed, initGreen, initBlack, initSilver, initOrange]

def kMeansColorSpace(arr, initColors):
    X = arr.reshape(1, -1, 3).squeeze() 
    return cluster.kMeans(X, initColors)    

def paletteTransformIm(im, palette):
    return m.pixelwiseIm(im, lambda pix: tuple(m.closest(pix, palette)))

def connectedComponents(arr, palette):
    components = np.zeros(arr.shape[0:2])
    numcomponents = 0
    for (i, color) in enumerate(palette):
        onecolor = m.pixelwiseArr(arr, lambda pix: (pix == color).all())[:,:,0] # all dimensions identical

        # remove specks
        erSize = 4;
        eroded = ndimage.binary_erosion(onecolor, structure=np.ones((erSize, erSize)))
        reconstructed = ndimage.binary_propagation(eroded, mask=onecolor)
        
        # find connected components
        (labels, numlabels) = ndimage.measurements.label(reconstructed)
        components = labels + m.pixelwiseArr(components, lambda x : 0 if x==0 else x+numlabels)
        numcomponents += numlabels
    return (components, numcomponents)

def test():
    m.loadIm('img2.bmp')
    print "Transforming palette"
    b = paletteTransformIm(m.im, allColors)
    print "Finding connected components"
    (c,n) = connectedComponents(np.array(b), allColors)
    print "Displaying result"
    plt.imshow(c)
    
    print "Removing small components"
    c = c.astype('int')
    sizes = ndimage.sum(c > 0, c, range(n+1))
    sizethresh = 100
    remove = (sizes<sizethresh)[c]
    c[remove] = 0 # todo - fill with neighbors instead?
    labels = np.unique(c)
    c = np.searchsorted(labels, c)

    print "Calculating centers of mass"
    com = ndimage.measurements.center_of_mass(c, c, range(1, len(np.unique(c))))
    return com
    #arr = np.array(m.im)
    #newMeans= s.kMeansColorSpace(m.downsample(arr, 10), allColors)
    #afterKmeans = paletteTransform(m.im, newMeans) # and this image
