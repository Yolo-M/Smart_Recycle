
"""File: echo_multi_sensor.py"""
# Import necessary libraries.
from time import sleep

from Bluetin_Echo import Echo

# Define pin constants
TRIGGER_PIN_1 = 13
ECHO_PIN_1 = 16
TRIGGER_PIN_2 = 26
ECHO_PIN_2 = 19
TRIGGER_PIN_3 = 6
ECHO_PIN_3 = 12
# Initialise three sensors.
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
    , Echo(TRIGGER_PIN_2, ECHO_PIN_2)
    , Echo(TRIGGER_PIN_3, ECHO_PIN_3)]


def main():
    sleep(0.1)
    while True:
        for counter2 in range(0, len(echo)):
            result = echo[counter2].read('cm', 4)
            print('Sensor {} - {} cm'.format(counter2, round(result, 2)))

    echo[0].stop()


if __name__ == '__main__':
    main()