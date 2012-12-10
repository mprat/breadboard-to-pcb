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
allColors = [initBeige, initRed, initGreen, initBlack, initBeige]

def kMeansColorSpace(arr, initColors): # HIGHLY recommended to downsample first!
    X = arr.reshape(1, -1, 3).squeeze() 
    return cluster.kMeans(X, initColors)    

def paletteTransform(im, palette):
    imPix = im.load()
    out = Image.new(im.mode, im.size)
    outPix = out.load()
    for x in range(out.size[0]):
        for y in range(out.size[1]):
            newColor = tuple(m.closest(imPix[x, y], palette))
            outPix[x, y] = newColor
    return out

# To test:
#arr = np.array(im)
#beforeKmeans = paletteTransform(im, allColors) # Look at this image
#newMeans= kMeansColorSpace(m.downsample(arr, 10), allColors)
#afterKmeans = paletteTransform(im, newMeans) # and this image
