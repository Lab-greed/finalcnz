import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN1 = 6
IN2 = 13 

IN3 = 23  
IN4 = 22

ENB = 21
ENA = 20

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
    
def down():
    GPIO.cleanup()
    GPIO.output(22,GPIO.LOW)
    
    
    
def up():
    GPIO.cleanup()
    GPIO.output(IN3,GPIO.LOW)  

   
down()
time.sleep(20)

#down()

GPIO.cleanup() 