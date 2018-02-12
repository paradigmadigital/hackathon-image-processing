import cv2
import numpy as np

img = cv2.imread("dataset/examples/apertura.png", 0)

cv2.imshow('Paradigma', img)
cv2.waitKey(0)

kernel = np.ones((5, 5), np.uint8)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

cv2.imshow('Paradigma', opening)
cv2.waitKey(0)
cv2.destroyAllWindows()
