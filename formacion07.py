from __future__ import absolute_import, division, print_function, unicode_literals

import cv2
import numpy as np

cap = cv2.VideoCapture("dataset/examples-video/test.mp4")

while (cap.isOpened()):
    ret, frame = cap.read()

    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    height = np.size(frame, 0)
    width = np.size(frame, 1)

    cv2.line(frame, (width, height // 10), (0, height // 10), (255, 0, 255), 5)
    cv2.line(frame, (width, (height // 10) * 9), (0, (height // 10) * 9), (255, 255, 0), 5)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
