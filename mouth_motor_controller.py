#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

MOUTH_PIN_1 = 37
MOUTH_PIN_2 = 35

class MouthMotorController():

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(MOUTH_PIN_1, GPIO.OUT)
        GPIO.setup(MOUTH_PIN_2, GPIO.OUT)

        self.all_stop()
        self.mouth_state = False

    def all_stop(self): 
        self.mouth_stop()

    ######  MOUTH #######
    def mouth_open(self):
        self.mouth_state = True
        GPIO.output(MOUTH_PIN_1, False)
        GPIO.output(MOUTH_PIN_2, True)
    
    def mouth_stop(self):
        self.mouth_state = False
        GPIO.output(MOUTH_PIN_1, True)
        GPIO.output(MOUTH_PIN_2, True)
