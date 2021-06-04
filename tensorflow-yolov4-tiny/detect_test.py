import time
import tensorflow as tf
import core.utils as utils
from tensorflow.python.saved_model import tag_constants
import cv2
import numpy as np

import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  #time 라이브러리의 sleep함수 사용

MODEL_PATH = './checkpoints/yolov4-tiny-416'
IOU_THRESHOLD = 0.45
SCORE_THRESHOLD = 0.50
INPUT_SIZE = 416

# load model
saved_model_loaded = tf.saved_model.load(MODEL_PATH, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']

servoPin1          = 16   # 서보1 핀
servoPin2          = 18  # 서보2 핀
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기

#GPIO
GPIO.setmode(GPIO.BOARD)        # GPIO 설정
GPIO.setup(servoPin1, GPIO.OUT)  # 서보핀 출력으로 설정
GPIO.setup(servoPin2, GPIO.OUT)  # 서보핀 출력으로 설정

servo1 = GPIO.PWM(servoPin1, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo1.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.

servo2 = GPIO.PWM(servoPin2, 50) 
servo2.start(0)  
'''
서보 위치 제어 함수
degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
'''
def setServoPos1(degree):
  # 각도는 180도를 넘을 수 없다.
  if degree > 180:
    degree = 180

  # 각도(degree)를 duty로 변경한다.
  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  # duty 값 출력
  print("Degree: {} to {}(Duty)".format(degree, duty))

  # 변경된 duty값을 서보 pwm에 적용
  servo1.ChangeDutyCycle(duty)
  
def setServoPos2(degree):
  # 각도는 180도를 넘을 수 없다.
  if degree > 180:
    degree = 180

  # 각도(degree)를 duty로 변경한다.
  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  # duty 값 출력
  print("Degree: {} to {}(Duty)".format(degree, duty))

  # 변경된 duty값을 서보 pwm에 적용
  servo2.ChangeDutyCycle(duty)  
  
def main(video_path):
    count = 0
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_input = cv2.resize(img, (INPUT_SIZE, INPUT_SIZE))
        img_input = img_input / 255.
        img_input = img_input[np.newaxis, ...].astype(np.float32)
        img_input = tf.constant(img_input)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        start_time = time.time()
        pred_bbox = infer(img_input)
       

        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=IOU_THRESHOLD,
            score_threshold=SCORE_THRESHOLD
        )

        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        result = utils.draw_bbox(img, pred_bbox)

        
        if valid_detections != 0:
            
            if classes[0][0] == 0:
                print("glass")
                setServoPos1(90)
                setServoPos2(120)
                time.sleep(1)
                
                
            elif classes[0][0] == 1:              
                print("metal")
                setServoPos1(50)
                setServoPos2(90)
                time.sleep(1)
                
            elif classes[0][0] == 2:              
                print("paper")
                setServoPos1(120)
                setServoPos2(180)
                time.sleep(1)
                
            elif classes[0][0] == 3:          
                print("plastic")
                setServoPos1(180)
                setServoPos2(50)
                time.sleep(1)
                
        """
        if valid_detections != 0:
           cv2.imwrite("./frames/frame%d.jpg" % count, img)
           count += 1
        """

        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)

        result = cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)


        cv2.imshow('result', result)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    video_path =0
    #./data/DASH_ROAD.mp4
    #0
    main(video_path)
