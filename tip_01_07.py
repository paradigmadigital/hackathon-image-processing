import cv2
from matplotlib import pyplot as plt

img = cv2.imread('dataset/examples/Holy-Grail2.jpg', 0)
bordes = cv2.Canny(img, 180, 260)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Imagen original'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(bordes, cmap='gray')
plt.title('Bordes de la Imagen'), plt.xticks([]), plt.yticks([])

plt.show()
