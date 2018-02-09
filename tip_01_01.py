import cv2
from matplotlib import pyplot as plt

img = cv2.imread("dataset/examples/Holy-Grail.jpg")
cv2.imshow("dataset/examples/Holy-Grail.jpg", img)
cv2.waitKey(0)
color = ('b', 'g', 'r')

for i, c in enumerate(color):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=c)
    plt.xlim([0, 256])

plt.show()

cv2.destroyAllWindows()
