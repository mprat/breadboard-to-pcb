import cv2

img = cv2.imread('../imgs/img1.jpg')
cv2.imshow('window_title', img)
cv2.waitKey(0)

#blob detection
sbd_params = cv2.SimpleBlobDetector_Params()

#display parameters in simple blob detector
# for p in sbd.getParams():
    # print p

#to modify any of the parameters below, just uncomment and change the value
# sbd_params.blobColor = 0
# sbd_params.filterByArea = 0
# sbd_params.filterByCircularity = 0
# sbd_params.filterByColor = 0
# sbd_params.filterByConvexity = 0
# sbd_params.filterByInertia = 0
# sbd_params.maxArea = 0
# sbd_params.maxCircularity = 0
# sbd_params.maxConvexity = 0
# sbd_params.maxInertiaRatio = 0
# sbd_params.maxThreshold = 0
# sbd_params.minDistBetweenBlobs = 0
# sbd_params.minRepeatability = 0
# sbd_params.minThreshold = 0
# sbd_params.thresholdStep = 0

print 'blobColor', sbd_params.blobColor
print 'filterByArea', sbd_params.filterByArea
print 'filterByCircularity', sbd_params.filterByCircularity
print 'filterByColor', sbd_params.filterByColor
print 'filterByConvexity', sbd_params.filterByConvexity
print 'filterByInertia', sbd_params.filterByInertia
print 'maxArea', sbd_params.maxArea
print 'maxCircularity', sbd_params.maxCircularity
print 'maxConvexity', sbd_params.maxConvexity
print 'maxInertiaRatio', sbd_params.maxInertiaRatio
print 'maxThreshold', sbd_params.maxThreshold
print 'minDistBetweenBlobs', sbd_params.minDistBetweenBlobs
print 'minRepeatability', sbd_params.minRepeatability
print 'minThreshold', sbd_params.minThreshold
print 'thresholdStep', sbd_params.thresholdStep

sbd = cv2.SimpleBlobDetector(sbd_params)
keypoints = sbd.detect(img) #returns an array of KeyPoints

#display keypoints on the original image
img3 = img.copy()
for kp in keypoints:
    #radius, color (B, G, R), line thickness
    cv2.circle(img3, tuple([int(coord) for coord in kp.pt]), 4, (0, 0, 255), 4)
cv2.imshow('keypoints_normal', img3)
cv2.waitKey(0)