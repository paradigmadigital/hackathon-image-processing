import cv2
import numpy as np

img = cv2.imread("dataset/examples/erosion-dilatation.png", 0)

cv2.imshow('Paradigma', img)
cv2.waitKey(0)

kernel = np.ones((5, 5), np.uint8)
dilation = cv2.dilate(img, kernel, iterations=1)

cv2.imshow('Paradigma', dilation)
cv2.waitKey(0)
cv2.destroyAllWindows()
