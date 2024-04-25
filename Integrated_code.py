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


upperservo =AngularServo(servo_pin3, min_pulse_width=0.0005, max_pulse_width=0.0023)
lowerservo =AngularServo(servo_pin1, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)

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
        #if not ret:
         #   print('Failed to capture')
          #  break
        if cv2.waitKey(1) & 0xFF==ord('c'):
            cv2.imwrite('/home/pi00/Major/image'+str(num)+'.jpg', img)
            print('Capture successful!')
            num +=  1
        if num == 4:
            break
    cap.release()
    cv2.destroyAllWindows()



def load_image(img_path):
    img = Image.open(img_path)
    img = img.resize((224, 224))
    img = np.array(img, dtype=np.float32)
    img /= 255.0
    img = np.expand_dims(img, axis=0)
    return img


def load_model(model_path):
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def use_model(path, model):
    new_image = load_image(path)
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    model.set_tensor(input_details[0]['index'], new_image)
    model.invoke()

    output_array = model.get_tensor(output_details[0]['index'])

    print("Prediction:", output_array)
    classes = ['metal', 'paper', 'plastic']
    predicted_class_index = np.argmax(output_array)
    predicted_class = classes[predicted_class_index]
    print("The waste in the image is classified as:", predicted_class)
    return predicted_class


try:
    while True:
        if GPIO.input(sensor):
            print("Yet to sense object...")
            while GPIO.input(sensor):
                time.sleep(0.2)
        else:
            print("Object Detected")
            captureImage()
            model_path = "/home/pi00/Major/roshanfinalmodel.tflite"
            image_path = f"/home/pi00/Major/image2.jpg"
            model = load_model(model_path)

            predicted_class = use_model(image_path, model)

            if predicted_class == 'plastic':
                lowerservo.angle=0
                time.sleep(2)
                
            elif predicted_class == 'paper':
                lowerservo.angle=90
                time.sleep(2)
            elif predicted_class == 'metal':
                lowerservo.angle=170
                time.sleep(2)
            else:
                lowerservo.angle=0
                time.sleep(2)
            upperservo.angle=80
            time.sleep(5)
            upperservo.angle=-80
            time.sleep(4)
            lowerservo.angle=0
            time.sleep(4)
            
except KeyboardInterrupt:
    GPIO.cleanup()