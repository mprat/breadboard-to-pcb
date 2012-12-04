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

TOREMEMBER:
* the numpy array and the python imaging library indices for the image are FLIPPED! (e.g. in numpy if you want to look up pixel i,j you do (arr[i], arr[j]) but in PIL you do im.putpixel((arr[j], arr[i]), (255, 255, 255))

TODO: 
* Rename the current "wire" class into "Component" and then make subclasses later
* Think of a better way of deciding whether to add RGB values to the wire. I think the best way to approach this for now is to keep a "running average" of an RGB color and threshold off of that.
