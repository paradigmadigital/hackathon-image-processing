# -*- coding: utf-8 -*-
# formacion10.py
import numpy as np
import cv2
from person import MyPerson
from collections import deque

line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)

resize = 0.5  # a la mitad

entran = 0
salen = 0

# pts=[]
pts = deque(maxlen=1024)


class MyFrame:
    def __init__(self, w, h):
        # Contadores de entrada y salida
        self.w = w
        self.h = h

        # Entry/Exit linees
        self.line_up = int(conf[0])  # 2
        self.line_down = int(conf[1])  # 3
        # Limit lines
        self.up_limit = int(conf[2])  # 1
        self.down_limit = int(conf[3])  # 4

    def getH(self):
        return self.h

    def getW(self):
        return self.w

    def getLineUp(self):
        return self.line_up

    def getLineDown(self):
        return self.line_down

    def getUpLimit(self):
        return self.up_limit

    def getDownLimit(self):
        return self.down_limit


def createHLine(top, width):
    pt1 = [0, top]
    pt2 = [width, top]
    pts_L1 = np.array([pt1, pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1, 1, 2))
    return pts_L1


# pts = deque(maxlen=args["buffer"])
# counter = 0
# (dX, dY) = (0, 0)
# direction = ""

cap = cv2.VideoCapture("..dataset/examples-video/VID_20180222_165601.mp4")

fgbg = cv2.createBackgroundSubtractorMOG2()

marta_cascade = cv2.CascadeClassifier('cascade.xml')

# Seteamos objeto frame
w = int(cap.get(3) * resize)
h = int(cap.get(4) * resize)

# lanes disposition
conf = [int(h / 2 - 10), int(h / 2 + 10), 5, h - 5]
myFrame = MyFrame(w, h)

# Seteamos informacion de personas
persons = []
max_p_age = 15
pid = 1
counter = 0
persons = 0

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # import ipdb;ipdb.set_trace()

    # frameHSV = np.zeros((h, w, 3), np.uint8)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_image = fgbg.apply(hsv)
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(h_image, cv2.MORPH_OPEN, kernel, iterations=2)
    # center = None

    bk = cv2.bitwise_and(frame, frame, mask=mask)

    # # Marker labelling
    # ret, markers = cv2.connectedComponents(sure_fg)
    # # Add one to all labels so that sure background is not 0, but 1
    # markers = markers + 1
    # # Now, mark the region of unknown with zero
    # markers[unknown == 255] = 0
    #
    # markers = cv2.watershed(img, markers)
    # img[markers == -1] = [255, 0, 0]

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        cv2.putText(bk, str(persons), (150, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 100:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(bk, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(bk, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

            # loop over the set of tracked points

            if len(pts) > 10:
                for i in np.arange(1, len(pts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if pts[i - 1] is None or pts[i] is None:
                        continue

                    # check to see if enough points have been accumulated in
                    # the buffer
                    if counter >= 10 and i == 1 and pts[-3] is not None and pts:
                        # compute the difference between the x and y
                        # coordinates and re-initialize the direction
                        # text variables
                        # dX = pts[-3][0] - pts[i][0]
                        dY = pts[-3][1] - pts[i][1]
                        # (dirX, dirY) = ("", "")
                        dirY = ""

                        # ensure there is significant movement in the
                        # x-direction
                        # if np.abs(dX) > 20:
                        #     dirX = "East" if np.sign(dX) == 1 else "West"

                        # ensure there is significant movement in the
                        # y-direction
                        if np.abs(dY) > 20:
                            dirY = "North" if np.sign(dY) == 1 else "South"

                        # handle when both directions are non-empty
                        direction = "{}".format(dirY) if dirY != "" else ""

                        # otherwise, compute the thickness of the line and
                        # draw the connecting lines
                        thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
                        cv2.line(bk, pts[i - 1], pts[i], (0, 0, 255), thickness)

                        # show the movement deltas and the direction of movement on
                        # the frame
                        cv2.putText(bk, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.65, (0, 0, 255), 3)
                        cv2.putText(bk, "dy: {}".format(dY),
                                    (10, bk.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.35, (0, 0, 255), 1)
                        if myFrame.getLineDown() < dY < myFrame.getLineUp():
                            persons += 1
                        elif myFrame.getLineDown() > dY > myFrame.getLineUp():
                            persons -= 1


    img_end = bk

    # Display the resulting frame
    cv2.imshow('Video', img_end)

    counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
