import Image
import ImageFilter
import cluster
import numpy as np
import main as m

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

def paletteTransform(im, palette):
    return m.pixelwise(im, lambda pix: tuple(m.closest(pix, palette)))

def connectedComponents(im, palette):
    # This does not work yet; it is just a stand-in
    def binaryTransform(px, color):
        if (px == palette[0]).all():
            return 1
        else:
            return 0
    return m.pixelwise(im, lambda x: binaryTransform(x, palette[0]), mode='1')


# To test:
#arr = np.array(m.im)
#beforeKmeans = s.paletteTransform(m.im, s.allColors) # Look at this image
#newMeans= s.kMeansColorSpace(m.downsample(arr, 10), allColors)
#afterKmeans = paletteTransform(m.im, newMeans) # and this image
