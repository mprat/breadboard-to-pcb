import cv2

img = cv2.imread('../imgs/img1.jpg')
cv2.imshow('window_title', img)
cv2.waitKey(0)

#blob detection
sbd = cv2.SimpleBlobDetector()

keypoints = sbd.detect(img) #returns an array of KeyPoints

#display keypoints on the original image
img3 = img.copy()
for kp in keypoints:
    #radius, color (B, G, R), line thickness
    cv2.circle(img3, tuple([int(coord) for coord in kp.pt]), 4, (0, 0, 255), 4)
cv2.imshow('keypoints_normal', img3)
cv2.waitKey(0)