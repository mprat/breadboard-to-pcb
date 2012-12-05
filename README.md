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
* it should work

TOREMEMBER:
* the numpy array and the python imaging library indices for the image are FLIPPED! (e.g. in numpy if you want to look up pixel i,j you do (arr[i], arr[j]) but in PIL you do im.putpixel((arr[j], arr[i]), (255, 255, 255))
* median filter is a fake segmentation implementation

TODO: 
* Rename the current "wire" class into "Component" and then make subclasses later
* use RANSAC to make component inclusion/exclusion deciding easier
* use sampling and color clustering to automatically decide on colors/thresholds (segmentation)
* auto-align birdseye view
* option to change between using running-average distance or "change the average in a significant way"
