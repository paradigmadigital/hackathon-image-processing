# coding=utf-8
import numpy as np
import cv2

cap = cv2.VideoCapture("dataset/examples-video/test.mp4")

# toma el 1º frame del video
ret, frame = cap.read()

# ajusta el tamño de la ventana
r, h, c, w = 300, 100, 500, 100  # simply hardcoded the values
track_window = (c, r, w, h)

# ajusta el ROI para el rastreo
roi = frame[r:r + h, c:c + w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Configure el criterio de terminación, ya sea 10 iteración o mover por lo menos 1 pt.
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while (1):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # aplica meanshift para conseguir la nueva ubicacion
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # dibuja en la imagen
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame, [pts], True, 255, 2)
        cv2.imshow('img2', img2)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k) + ".jpg", img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()