#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import rospy
import torch
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import os

model_path = os.getcwd() + '/weed_detection/weed_detection_ws/src/weed_detection/src/custom3.pt'

def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/sharnali/weed_detection/weed_detection_ws/src/weed_detection/src/custom3.pt', force_reload= True)
    return model

model = load_model()

def object_detector():
    bridge = CvBridge()
    cap = cv.VideoCapture(-1)
    rospy.init_node('image_process_publish', anonymous=True)
    bbox_pub = rospy.Publisher('weed_detection', Image, queue_size=10)

    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        # Read a frame from the camera
        ret, frame = cap.read()
        if ret:
            results = model(frame)
            ros_img = bridge.cv2_to_imgmsg(results.render()[0], encoding="passthrough")
            # Publish the image
            bbox_pub.publish(ros_img)
            rate.sleep()

    cap.release()

if __name__ == '__main__':
    try:
        object_detector()
    except rospy.ROSInterruptException:
        pass

    #ok
