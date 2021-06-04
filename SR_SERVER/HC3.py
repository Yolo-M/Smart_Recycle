from time import sleep
from Bluetin_Echo import Echo
import time
import socket

host = '127.0.0.1'  # 호스트 IP
port = 8888  # 포트번호 임의 설정

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((host, port))
server_sock.listen(10)

TRIGGER_PIN_1 = 13
ECHO_PIN_1 = 16
TRIGGER_PIN_2 = 26
ECHO_PIN_2 = 19
TRIGGER_PIN_3 = 6
ECHO_PIN_3 = 12

echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
    , Echo(TRIGGER_PIN_2, ECHO_PIN_2)
    , Echo(TRIGGER_PIN_3, ECHO_PIN_3)]

def main():
    sleep(0.1)
    print('starting server...')
    while True:
        connection, client_address = server_sock.accept()
        while True:
            
            for counter2 in range(0, len(echo)):
                result = echo[counter2].read('cm', 4)
                print('Sensor {} - {} cm'.format(counter2, round(result, 2)))
                server.sock.send(str(round(result, 2)))
                
            echo[0].stop()

if __name__ == '__main__':
    main()