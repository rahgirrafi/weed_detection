#!/usr/bin/env python3

import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch


def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path="/media/rafi/Technical/Projects/weed_detection/weed_detection_ws/src/weed_detection/src/custom3.pt", force_reload= True)
    return model

model = load_model()

def callback(data):
    bridge = CvBridge()
    # Convert the image message to an OpenCV image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    print(frame)
    results = model(frame)
    cv.imshow("Image window", results.render()[0])
    cv.waitKey(1)


rospy.init_node('image_process_subscribe', anonymous=True)
sub = rospy.Subscriber('weed_detection', Image, callback)
rospy.spin()
