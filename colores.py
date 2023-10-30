import cv2
import numpy as np
#funcion para dibujar las figuras o contornos
def draw(rostro, color,frame_c):
    contours,_=cv2.findContours(rostro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000:
            new_contours = cv2.convexHull(c)
            cv2.drawContours(frame_c,[new_contours],0,color,3)
            M=cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int (M["m10"]/M["m00"])
            y = int (M['m01']/M['m00'])
            font = cv2.FONT_HERSHEY_COMPLEX
            if color == [0,255,255]:
                cv2.putText(frame_c, 'Amarillo', (x+10, y),font, 0.75, (0,255,255),1, cv2.LINE_AA)
            elif color == [0,0,255]:
                cv2.putText(frame_c, 'Rojo', (x+10, y),font, 0.75, (0,0,255),1, cv2.LINE_AA)   
            elif color == [255,0,0]:
                cv2.putText(frame_c, 'Azul', (x+10, y),font, 0.75, (255,0,0),1, cv2.LINE_AA)

#funcion para que habra la camara y pueda capturar los colores
def capturando():
    capturar =cv2.VideoCapture(0)
    amarillo_bajo = np.array([20,190,20],np.uint8)
    amarillo_fuerte = np.array([30,255,255],np.uint8)

    azul_bajo = np.array([85,200,20], np.uint8)
    azul_fuerte=np.array([125,255,255], np.uint8)

    verde_bajo=np.array([45,100,20], np.uint8)
    verde_fuerte=np.array([75,255,255], np.uint8)

    rojo_bajo1 = np.array([0,100,20],np.uint8)
    rojo_fuerte1 = np.array([5,255,255],np.uint8)

    rojo_bajo2 = np.array([175,100,20],np.uint8)
    rojo_fuerte2 = np.array([179,255,255],np.uint8)

    while True:
        comp,frame=capturar.read()
        if comp==True:
            frame_HSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mascara_amarilla=cv2.inRange(frame_HSV,amarillo_bajo,amarillo_fuerte)
            mascara_azul=cv2.inRange(frame_HSV,azul_bajo,azul_fuerte)
            mascara_verde=cv2.inRange(frame_HSV,verde_bajo,verde_fuerte)
            mascara_rojo1=cv2.inRange(frame_HSV,rojo_bajo1,rojo_fuerte1)
            mascara_rojo2=cv2.inRange(frame_HSV,rojo_bajo2,rojo_fuerte2)
            mascara_rojas=cv2.add(mascara_rojo1,mascara_rojo2)

            draw(mascara_amarilla,(0,255,255),frame)
            draw(mascara_azul,(255,0,0),frame)
            draw(mascara_verde,(0,143,57), frame)
            draw(mascara_rojas,(0,0,255), frame)

            cv2.imshow('TecCam',frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
            capturar.release()
            cv2.destroyAllWindows()
