import os
import numpy as np
import RPi.GPIO as GPIO
import time
import cv2  # Add import for cv2
from time import sleep
import subprocess
import datetime
import matplotlib.pyplot as plt
from PIL import Image
import tflite_runtime.interpreter as tflite
from gpiozero import AngularServo
num =2
buzzer = 22
servo_pin3 = 27
servo_pin1 = 24
sensor = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin3, GPIO.OUT)
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

dt = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
dateStr, timeStr = dt.split()


def captureImage():
    num=2 
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, img = cap.read()
        cv2.imshow('Frame',img)
        if not ret:
            print('Failed to capture')
            break
        if cv2.waitKey(1) & 0xFF==ord('c'):
            cv2.imwrite('/home/pi00/Major/image'+str(num)+'.jpg', img)
            print('Capture successful!')
            num +=  1
        if num == 4:
            break
    cap.release()
    cv2.destroyAllWindows()

captureImage()

