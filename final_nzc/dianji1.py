import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN1 = 6
IN2 = 13 

IN3 = 19  
IN4 = 26

IN5 = 21
IN6 = 20

def init():
    GPIO.setup(IN1, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN5, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN6, GPIO.OUT,initial=GPIO.LOW)
    
    
#GPIO.setup(ENB,GPIO.OUT)
#p1=GPIO.PWM(ENB,100)
#p1.start(50)

#GPIO.setup(ENA,GPIO.OUT)
#p2=GPIO.PWM(ENA,100)
#p2.start(50)

init()    
    
def up():
    
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    
    
def down():
   
    GPIO.output(IN3, GPIO.HIGH)  
    GPIO.output(IN4,GPIO.LOW)


def pull():
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    
def push():
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN1,GPIO.LOW)
    
def a_down():
    GPIO.output(IN5,GPIO.HIGH)
    GPIO.output(IN6,GPIO.LOW)
    
def a_up():
    GPIO.output(IN6,GPIO.HIGH)
    GPIO.output(IN5,GPIO.LOW)
    
    
def get_up():
    push()
    time.sleep(2.4)
    init()
    time.sleep(0.2)
    up()
    time.sleep(6)
    push()
    time.sleep(0.6)
    
def lay_down():
    down()    
    time.sleep(5.488)
    init()
    time.sleep(0.2)
    pull()
    time.sleep(6)
    
def arm_down():
    a_down()
    time.sleep(5.8)
    
def arm_up():
    a_up()
    time.sleep(6)
    
    
    
init()



#get_up()
#time.sleep(2)
#lay_down()


#push()    
#time.sleep(600)


#a_up()
#time.sleep(1)
#init()


#init()
#time.sleep(3)
#a_up()
#time.sleep(0.2)
#a_down()
#time.sleep(6)
#init()
#time.sleep(3)
#down()    
#time.sleep(4.93)

pull()
time.sleep(0.6)
#push()
#time.sleep(0.6)
#up()
#time.sleep(6)
#pull()
#time.sleep(0.2)
#down()
#time.sleep(5.47)
#down()
#time.sleep(0.2)

init()


