import RPi.GPIO as gpio
import time


frt_trig = 26
frt_echo = 19

rig_trig = 13
rig_echo = 16

lef_trig = 6
lef_echo = 12


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)


gpio.setup(frt_trig, gpio.OUT)
gpio.setup(rig_trig, gpio.OUT)
gpio.setup(lef_trig, gpio.OUT)

gpio.setup(frt_echo, gpio.IN)
gpio.setup(rig_echo, gpio.IN)
gpio.setup(lef_echo, gpio.IN)


def dist(trig, echo):
    global srt, end

    gpio.output(trig, False)
    time.sleep(0.5)
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    while gpio.input(echo) == 0:
        srt = time.time()

    while gpio.input(echo) == 1:
        end = time.time()

    puls_drtn = end - srt
    distance = puls_drtn * 17000
    distance = round(distance, 2)


while True:
    frt_dist = dist(frt_trig,frt_echo)
    rig_dist = dist(rig_trig,rig_echo)
    lef_dist = dist(lef_trig,lef_echo)
    print("frt_Distance : {} cm / rig_Distance : {} cm / lef_Distance : {} cm".format(frt_dist, rig_dist, lef_dist))
    #print(frt_dist, "cm", rig_dist, "cm", lef_dist, "cm")
    #print("fist-distance: {} cm / second-distance: {} cm/ third-distance: {} cm".format(frt_dist,snd_dist,trd_dist))

