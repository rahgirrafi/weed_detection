#!/usr/bin/env python3

import cv2 as cv
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

gps =  ''
def gps_callback(data):
    global gps
    gps = data.data   

def callback(data):
    bridge = CvBridge()
    gps_sub = rospy.Subscriber('gps', String, gps_callback)
    # Convert the image message to an OpenCV image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    frame = frame.copy()    
    print(frame)
    frame = cv.putText(frame, gps, (0,25), cv.FONT_HERSHEY_COMPLEX, 0.5 , (0,0,0), 1, cv.LINE_AA)
    
    cv.imshow("Image window", frame)
    cv.waitKey(1)


rospy.init_node('image_subscribe', anonymous=True)
sub = rospy.Subscriber('weed_detection', Image, callback)
rospy.spin()
