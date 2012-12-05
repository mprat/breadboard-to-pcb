import Image
import ImageFilter

def modeSegment(im):
	#can get an image without the holes in the breadboard from a modefilter
	#the number is hard-coded and made up for now
	immodefilter = im.filter(ImageFilter.ModeFilter(10))
	return immodefilter	
	#showImg(immodefilter, showstr)
	

