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

GPIO.output(buzzer, False)
print("IR Sensor Ready.....")
print(" ")

while True:
    upperservo =AngularServo(servo_pin3, min_pulse_width=0.0005, max_pulse_width=0.0023)
    lowerservo =AngularServo(servo_pin1, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
    
    print("upper at 0")
    upperservo.angle=0
    
    time.sleep(5)
    print("lower at 0")
    lowerservo.angle=0
    
    time.sleep(4)
    print("upper at 80")
    upperservo.angle=80
    
    
    time.sleep(5)
    print("lower at 90")
    lowerservo.angle=90
    
    time.sleep(4)
    print("upper at 0")
    upperservo.angle=0
    time.sleep(5)
    print("lower at 170")
    lowerservo.angle=170
    time.sleep(4)
    print("upper at -80")
    upperservo.angle=-80
    time.sleep(5)
    
    print("lower at 0")
    lowerservo.angle=0    
    time.sleep(5)
    print("lower at 0")
    upperservo.angle=0
    time.sleep(4)