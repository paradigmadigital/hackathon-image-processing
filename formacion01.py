import cv2

imagePath = "dataset/examples/Holy-Grail.jpg"
img = cv2.imread(imagePath, 0)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
