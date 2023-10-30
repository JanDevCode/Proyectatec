import cv2
import os
import imutils

persona = 'Antonio'
data_path = 'Data_Face'
persona_path = data_path + '/' + persona

if not os.path.exists(persona_path):
    os.makedirs(persona_path)

capture = cv2.VideoCapture('')#video de mi rostro

face_classif = cv2.CascadeClassifier('')