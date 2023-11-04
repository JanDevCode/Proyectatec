import cv2
import numpy as np
#funcion para dibujar las figuras o contornos
def draw(rostro, color,frame_arg):
    contours,_=cv2.findContours(rostro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000:
            new_contours = cv2.convexHull(c)
            cv2.drawContours(frame_arg,[new_contours],0,color,3)
#funcion para que habra la camara y pueda capturar los colores
def capturando():
    capturar =cv2.VideoCapture(0)
    amarillo_bajo = np.array([25,192,20],np.uint8)
    amarillo_fuerte = np.array([30,255,255],np.uint8)
    rojo_bajo1 = np.array([0,100,20],np.uint8)
    rojo_fuerte1 = np.array([5,255,255],np.uint8)
    rojo_bajo2 = np.array([175,100,20],np.uint8)
    rojo_fuerte2 = np.array([180,255,255],np.uint8)

    while True:
        comp,frame=capturar.read()
        if comp==True:
            frame_HSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mascara_amarilla=cv2.inRange(frame_HSV,amarillo_bajo,amarillo_fuerte)
            mascara_rojo1=cv2.inRange(frame_HSV,rojo_bajo1,rojo_fuerte1)
            mascara_rojo2=cv2.inRange(frame_HSV,rojo_bajo2,rojo_fuerte2)
            mascara_roja=cv2.add(mascara_rojo1,mascara_rojo2)

            draw(mascara_amarilla, [0,255,255],frame)
            draw(mascara_roja, [0,0,255], frame)

            cv2.imshow('TecCam',frame)

            if cv2.waitKey(3) & 0xFF == ord('w'):
                break
            capturar.release()
            cv2.destroyAllWindows()
