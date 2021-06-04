import time
import tensorflow as tf
import core.utils as utils
from tensorflow.python.saved_model import tag_constants
import cv2
import numpy as np

MODEL_PATH = './checkpoints/yolov3-416-tiny'
IOU_THRESHOLD = 0.45
SCORE_THRESHOLD = 0.35
INPUT_SIZE = 416

# load model
saved_model_loaded = tf.saved_model.load(MODEL_PATH, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']

def main(video_path):
    count = 0
    cap = cv2.VideoCapture(video_path)
    #cap.set(3,640)
    #cap.set(4,480)

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
                
            elif classes[0][0] == 1:              
                print("metal")                
                
            elif classes[0][0] == 2:              
                print("paper")                
                
            elif classes[0][0] == 3:          
                print("plastic")
                
 
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
    video_path = 0
    main(video_path)
