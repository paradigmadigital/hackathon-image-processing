from __future__ import absolute_import, division, print_function, unicode_literals

import cv2

cap = cv2.VideoCapture("dataset/examples-video/test.mp4")

fgbg = cv2.createBackgroundSubtractorMOG2()
while (cap.isOpened()):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(30) & 0xff
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
