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

from RPLCD.i2c import CharLCD  # Import the LCD library



buzzer = 22

servo_pin3 = 17

servo_pin1 = 27

sensor = 18

trig_pin = 23  # Ultrasonic sensor trigger pin

echo_pin = 24  # Ultrasonic sensor echo pin



GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_pin3, GPIO.OUT)

GPIO.setup(servo_pin1, GPIO.OUT)

GPIO.setup(sensor, GPIO.IN)

GPIO.setup(buzzer, GPIO.OUT)

GPIO.setup(trig_pin, GPIO.OUT)

GPIO.setup(echo_pin, GPIO.IN)



GPIO.output(buzzer, False)

print("IR Sensor Ready.....")

print(" ")



upperservo =AngularServo(servo_pin3, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)

lowerservo =AngularServo(servo_pin1, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)



dt = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

dateStr, timeStr = dt.split()



# Set up LCD display

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)



def measure_distance():

    # Trigger the ultrasonic sensor

    GPIO.output(trig_pin, True)

    time.sleep(0.00001)

    GPIO.output(trig_pin, False)



    # Measure the time it takes for the echo to return

    pulse_start_time = time.time()

    while GPIO.input(echo_pin) == 0:

        pulse_start_time = time.time()



    pulse_end_time = time.time()

    while GPIO.input(echo_pin) == 1:

        pulse_end_time = time.time()



    # Calculate distance in centimeters

    pulse_duration = pulse_end_time - pulse_start_time

    distance = pulse_duration * 17150

    distance = round(distance, 2)



    return distance



def display_distance(distance):

    lcd.clear()

    lcd.write_string(f"Distance: {distance} cm")



def captureImage():

    num = 2

    cap = cv2.VideoCapture(0)



    while True:

        ret, img = cap.read()

        if cv2.waitKey(1):

            cv2.imwrite('/home/pi99/Major/image' + str(num) + '.jpg', img)

            print('Capture successful!')

            num = num + 1

        if num == 3:

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

    classes = ['metal', 'plastic', 'paper']

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

            

            model_path = "/home/pi99/Major/lite.tflite"

            image_path = "/home/pi99/Major/image2.jpg"

            model = load_model(model_path)



            predicted_class = use_model(image_path, model)

            # Measure distance and display it on the LCD

            distance = measure_distance()

            display_distance(distance)

            

            if distance<=5.5:

                lcd.write_string(f"Full Bin")

            else:

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

                upperservo.angle=170

                time.sleep(5)

                upperservo.angle=170

                time.sleep(4)

                lowerservo.angle=0

                time.sleep(4)

            lcd.clear()

except KeyboardInterrupt:

    GPIO.cleanup()



    



