import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

trig1 = 2
echo1 = 3

trig2 = 27
echo2 = 22

trig3 = 5
echo3 = 6

GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)

GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(echo2, GPIO.IN)

GPIO.setup(trig3, GPIO.OUT)
GPIO.setup(echo3, GPIO.IN)

def dist(trig, echo) :
    global srt, end

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

    if distance > 100:
        distance = 100;


while True :
    first_dist = dist(trig1,echo1)
    second_dist = dist(trig2, echo2)
    third_dist = dist(trig3, echo3)

    print("fist-distance: {} cm /\n second-distance: {} cm/\n third-distance: {} cm\n"
          .format(first_dist,second_dist,third_dist))

