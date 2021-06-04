import RPi.GPIO as GPIO
import time
import socket

host = '127.0.0.1'  # 호스트 IP
port = 8888  # 포트번호 임의 설정
GPIO.setmode(GPIO.BCM)

# GPIO_TRIGGER = 18
# GPIO_ECHO = 24

GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((host, port))
server_sock.listen(1)

# sock.connect(("127.0.0.1", 6666))

while True:
    connection, client_address = server_sock.accept()
    try:
        print("Connected: " + client_address)
        GPIO.output(26, True)
        time.sleep(0.00001)
        GPIO.output(26, False)
        
        while GPIO.input(16) == 0:
            StartTime = time.time()
            
        while GPIO.input(16) == 1:
            TimeElapsed = StopTime - time.time()
            # distance = (TimeElapsed * 34300) / 2
            distance = (TimeElapsed * 34029) / 2
            # print("Distance: "+str(distance))
            n = server.sock.send(str(distance))
            
    except:
        print("Bye")
        GPIO.cleanup()
        server.sock.close()
        break
