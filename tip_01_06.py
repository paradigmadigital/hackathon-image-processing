import cv2
import numpy as np

img = cv2.imread('dataset/examples/contours.png')
# img = cv2.resize(i, (0, 0), fx=0.3, fy=0.3)
cv2.imshow("Show", img)
cv2.waitKey()

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower mask (0-10)
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
mask0 = cv2.inRange(hsv_img, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([170, 130, 130])
upper_red = np.array([180, 255, 255])
mask1 = cv2.inRange(hsv_img, lower_red, upper_red)

# join my masks
mask = mask0 + mask1

# set my output img to zero everywhere except my mask
output_img = img.copy()
output_img[np.where(mask == 0)] = 0

# or your HSV image, which I *believe* is what you want
output_hsv = hsv_img.copy()
output_hsv[np.where(mask == 0)] = 0

ret, thresh = cv2.threshold(output_hsv, 127, 255, 0)
cv2.imshow("Show", thresh)
cv2.waitKey()
gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

image, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

cv2.imshow("Show", img)
cv2.waitKey()
cv2.destroyAllWindows()
