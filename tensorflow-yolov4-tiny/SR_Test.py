import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)

trig1 = 26
echo1 = 19

trig2 = 13
echo2 = 16

trig3 = 6
echo3 = 12


GPIO.setup(trig, GPIO.OUT)

GPIO.setup(echo, GPIO.IN)

#try :
while True :
    GPIO.output(trig, False)
    time.sleep(0.5)

    GPIO.output(trig, True)
    time.sleep(0.00001)

    GPIO.output(trig, False)

    while GPIO.input(echo) == 0 :
        pulse_start = time.time()

    while GPIO.input(echo) == 1 :
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17000

    distance = round(distance, 2)

    print("거리 : ", distance, "cm")

#except Keyboardinterrupt :
 #    GPIO.cleanup()