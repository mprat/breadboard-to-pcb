breadboard-to-pcb
=================

Python program to transform a picture of a neat breadboarded circuit into a
PCB-layout in some way.

The program requires the Python Imaging Library
(http://www.pythonware.com/products/pil/), and right now only BMP images have
been tested.

You must also install the python-tk package on your computer. In Ubuntu, sudo
apt-get install python-tk does the trick.

The way to run the command-line python program is to run

python main.py imgname.bmp show

If the last argument is "show" then any debugging code to show the outputs of
the images will be run. Otherwise, you will not see any images on the screen.

INSTALLNOTES:
* to get Tkinter to work in python, run
sudo apt-get install tk8.5-dev tcl8.5-dev python-tk
* download PIL and run python setup.py install in the directory after you uncompress it
* need to do sudo apt-get install python-matplotlib to get matplotlib to work
* install Lapack - sudo apt-get install liblapack-dev

TOREMEMBER:
* the numpy array and the python imaging library indices for the image are FLIPPED! (e.g. in numpy if you want to look up pixel i,j you do (arr[i], arr[j]) but in PIL you do im.putpixel((arr[j], arr[i]), (255, 255, 255))
* median filter is a fake segmentation implementation

TODO: 
* use sampling and color clustering to automatically decide on colors/thresholds (segmentation)
* auto-align birdseye view
* option to change between using running-average distance or "change the average in a significant way" (RANSAC)
* differentiate between components
* where the user clicks, generate a few "component models" and ask the user to choose the best one?


====================
(Michele and Robin's hacking)

Decent set of parameters to start detecting blobs with:

```
sbd_params = cv2.SimpleBlobDetector_Params()
        sbd_params.blobColor = 0
        sbd_params.filterByArea = True
        sbd_params.filterByCircularity = False
        sbd_params.filterByColor = True
        sbd_params.filterByConvexity = False
        sbd_params.filterByInertia = False
        sbd_params.maxArea = 100
        sbd_params.minArea = 10
        sbd_params.maxCircularity = 0
        sbd_params.minCircularity = 0
        sbd_params.maxConvexity = 0
        sbd_params.minConvexity = 0
        sbd_params.maxInertiaRatio = 0
        sbd_params.minInertiaRatio = 0
        sbd_params.maxThreshold = 100
        sbd_params.minThreshold = 10
        sbd_params.minDistBetweenBlobs = 10
        sbd_params.minRepeatability = 2
        sbd_params.thresholdStep = 10
```
