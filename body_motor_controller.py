#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

HEAD_PIN_1 = 38
HEAD_PIN_2 = 40
TAIL_PIN_1 = 11
TAIL_PIN_2 = 13

# NOTE: My power supply can only drive two motors at a time 
#       So I will only use either the head motor or tail motor 
#       at the same time. 
class BodyMotorController():

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(HEAD_PIN_1, GPIO.OUT)
        GPIO.setup(HEAD_PIN_2, GPIO.OUT)
        GPIO.setup(TAIL_PIN_1, GPIO.OUT)
        GPIO.setup(TAIL_PIN_2, GPIO.OUT)

        self.all_stop()
        self.head_state = False
        self.tail_state = False

    def all_stop(self): 
        self.head_stop()
        self.tail_stop()

    ######  HEAD  #######
    def head_out(self):
        # This is to prevent all three motors from being active at the same time
        self.tail_stop()

        self.head_state = True
        GPIO.output(HEAD_PIN_1, False)
        GPIO.output(HEAD_PIN_2, True)
    
    ### NOTE:  There is a retraction mechanism on the fish.  
    ###        We can move the head or tail in by setting motor voltage to 0
    ###        Same thing with the mouth. 
    def head_stop(self):
        self.head_state = False
        GPIO.output(HEAD_PIN_1, True)
        GPIO.output(HEAD_PIN_2, True)
    
    ######  TAIL  #######
    def tail_out(self):
        if self.head_state:
            print("Tail disabled when head is out")
            return

        self.tail_state = True
        GPIO.output(TAIL_PIN_1, True)
        GPIO.output(TAIL_PIN_2, False)
    
    def tail_stop(self):
        self.tail_state = False
        GPIO.output(TAIL_PIN_1, True)
        GPIO.output(TAIL_PIN_2, True)
    
if __name__ == "__main__":
    mc = BodyMotorController()
    import code
    code.interact(local=locals())
