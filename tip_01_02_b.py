import cv2
from matplotlib import pyplot as plt

# Ecualizacion de histogramas
img = cv2.imread("dataset/examples/life-of-brian2.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.equalizeHist(img)

cv2.imshow('Histogramas', img)
cv2.waitKey(0)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(hist, color='gray')

plt.xlabel('intensidad de iluminacion')
plt.ylabel('cantidad de pixeles')
plt.show()
