import RPi.GPIO as GPIO
import time
import smbus
from RPLCD.i2c import CharLCD

# Ultrasonic sensor pins
TRIG = 23
ECHO = 24

# LCD display configuration
lcd = CharLCD('PCF8574', 0x27)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

try:
    while True:
        distance = measure_distance()
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Distance: {} cm".format(distance))
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()

