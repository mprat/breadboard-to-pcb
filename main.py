import Image
import sys

# write name of file in command-line arguments
if (len(sys.argv) > 2):
	sys.exit(0)
else:
	filename = sys.argv[1]
	im = Image.open("imgs/"+ filename)
	im.show()
