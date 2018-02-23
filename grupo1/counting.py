# coding=utf-8
import json
import time

import cv2
import numpy as np
from imutils.video import VideoStream

import Person


class MyFrame:
    def __init__(self, w, h):
        # Contadores de entrada y salida
        self.w = w
        self.h = h

        coord = h
        if currentConfiguration[1] == 0:  # horizontal
            coord = w

        # Entry/Exit linees
        self.line_up = int(currentConfiguration[3] * (coord / 5))  # 2
        self.line_down = int(currentConfiguration[4] * (coord / 5))  # 3
        # Limit lines
        self.up_limit = int(currentConfiguration[5] * (coord / 5))  # 1
        self.down_limit = int(currentConfiguration[6] * (coord / 5))  # 4

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


def createVLine(xValue):
    pt1 = [xValue, 0];
    pt2 = [xValue, h];
    pts_L1 = np.array([pt1, pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1, 1, 2))
    return pts_L1


def createHLine(yValue):
    pt1 = [0, yValue];
    pt2 = [w, yValue];
    pts_L1 = np.array([pt1, pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1, 1, 2))
    return pts_L1


def emitEvent(direction):
    message = {}
    message['deviceId'] = "dev1"
    message['direction'] = direction
    message['location'] = "startrek"
    message['dateTime'] = time.strftime("%c")
    messageJson = json.dumps(message)
    print(message)


# Configuracion de video: video, direccion, scaleFactor, line_up, line_down, up_limit, down_limit

conf = []
conf.append(['videos/myself.webm', 0, 20, 1, 4, 0.2, 4.8])  # 0 -> Horiozntal de mi mismo (grande)
conf.append(['videos/peopleCounterH.avi', 0, 250, 2, 3, 1, 4])  # 1 -> Horiozntal de mi mismo (grande)
conf.append(['videos/peopleCounter.avi', 1, 250, 2, 3, 1, 4])  # 2 -> Vertical del vídeo de siempre (pequeño)
conf.append(
    ['../dataset/examples-video/VID_20180222_165601.mp4', 1, 20, 2, 3, 0.8, 4.2])  # 3 -> Vertical sin vídeo asociado (cámara Paradigma)

conf.append(
    ['videos/puerta/test3.mp4', 1, 20, 1.4, 3.6, 0.6, 4.4])  # 4 -> Vertical sin vídeo asociado (cámara Paradigma)

confLabels = []
confLabels.append(['LEFT', 'RIGHT'])  # direction -> 0
confLabels.append(['UP', 'DOWN'])  # direction -> 1

# Parametros de inicializacion

#############################
# Values: 0, 1, 2
##############################
currentConfiguration = conf[3]
piCamera = False
runningVideo = True

##############################

direction = currentConfiguration[1]
currentLabelConfiguration = confLabels[direction]

if (runningVideo):
    cap = cv2.VideoCapture(currentConfiguration[0])
else:
    vs = VideoStream(usePiCamera=piCamera).start()

time.sleep(2)

if (piCamera):
    w = vs.camera.resolution.width
    h = vs.camera.resolution.height
    vs.camera.rotation = 180
    cap = vs
else:
    if 'vs' in locals():
        cap = vs.stream

    # Imprime las propiedades de captura a consola
    for i in range(19):
        print(i, cap.get(i))
    w = cap.get(3)
    h = cap.get(4)

frameArea = h * w

# Min area size to recognize it as a Person
areaTH = frameArea / currentConfiguration[2]  # frameArea/250
print('Area Threshold', areaTH)

myFrame = MyFrame(w, h)

print("Red line y:", str(myFrame.getLineDown()))
print("Blue line y:", str(myFrame.getLineUp()))
line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)

# Creating the lines
if currentConfiguration[1] == 1:  # vertical
    pts_L1 = createHLine(myFrame.getLineDown())
    pts_L2 = createHLine(myFrame.getLineUp())
    pts_L3 = createHLine(myFrame.getUpLimit())
    pts_L4 = createHLine(myFrame.getDownLimit())
else:
    pts_L1 = createVLine(myFrame.getLineDown())
    pts_L2 = createVLine(myFrame.getLineUp())
    pts_L3 = createVLine(myFrame.getUpLimit())
    pts_L4 = createVLine(myFrame.getDownLimit())

# Substractor de fondo
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

# Elementos estructurantes para filtros morfologicos
kernelOp = np.ones((3, 3), np.uint8)
kernelOp2 = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

# Variables
font = cv2.FONT_HERSHEY_SIMPLEX

persons = []
# Max num of frames without detecting a person before deleting it
max_p_age = 5
pid = 1

while (True):  # cap.isOpened()):

    # Lee una imagen de la fuente de video
    if (piCamera):
        frame = cap.read()
    else:
        ret, frame = cap.read()

    # increasing age every person one frame
    for i in persons:
        i.age_one()

    #########################
    #   PRE-PROCESAMIENTO   #
    #########################

    # Aplica substraccion de fondo
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    # Binariazcion para eliminar sombras (color gris)
    try:
        ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        ret, imBin2 = cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)
        # Opening (erode->dilate) para quitar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
        # Closing (dilate -> erode) para juntar regiones blancas.
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        break
    #################
    #   CONTORNOS   #
    #################

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    _, contours0, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours0, -1, (0, 255, 0), 20)

    """  """
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        # Only if the area is big enough
        if area > areaTH:
            #################
            #   TRACKING    #
            #################
            height, width = frame.shape[:2]
            # Falta agregar condiciones para multipersonas, salidas y entradas de pantalla.

            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)
            new = True
            # if y + h < height:
            coord = cy
            if currentConfiguration[1] == 0:  # horizontal
                coord = cx

            if coord in range(myFrame.getUpLimit(), myFrame.getDownLimit()):
                for i in persons:
                    # Checking if the contour belongs to the person
                    if abs(cx - i.getX()) <= w and abs(cy - i.getY()) <= h:
                        # el objeto esta cerca de uno que ya se detecto antes
                        new = False
                        i.updateCoords(cx, cy)  # actualiza coordenadas en el objeto and resets age
                        if i.going_UP(myFrame.getLineDown(), myFrame.getLineUp(), direction) == True:
                            emitEvent(currentLabelConfiguration[0])  # UP
                        elif i.going_DOWN(myFrame.getLineDown(), myFrame.getLineUp(), direction) == True:
                            emitEvent(currentLabelConfiguration[1])  # DOWN
                        break

                    # TODO all the code below should be probably outside this loop
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > myFrame.getDownLimit():
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < myFrame.getUpLimit():
                            i.setDone()
                    if i.timedOut():
                        # sacar i de la lista persons
                        index = persons.index(i)
                        persons.pop(index)
                        del i  # liberar la memoria de i
                if new == True:
                    p = Person.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1
            #################
            #   DIBUJOS     #
            #################
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

    # END for cnt in contours0

    #################
    #   IMAGENES    #
    #################

    frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
    frame = cv2.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)

    frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
    cv2.imshow('Frame', frame)

    # preisonar ESC para salir
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        import time

        time.sleep(0.9)
# END while(cap.isOpened())

#################
#   LIMPIEZA    #
#################
if (piCamera):
    cap.stop()
else:
    cap.release()
cv2.destroyAllWindows()
