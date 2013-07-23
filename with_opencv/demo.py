import cv2

img = cv2.imread('../imgs/img1.jpg')
cv2.imshow('window_title', img)
cv2.waitKey(0)