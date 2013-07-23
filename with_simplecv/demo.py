import SimpleCV
image = SimpleCV.Image('../imgs/img1.jpg')
p = image.getPalette()
blobs = image.findBlobsFromPalette(p[0])
b = blobs[0]
print b.hull()
b.drawHull()
while True:
    image.show()