#!/usr/bin/env python3

import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def callback(data):
    bridge = CvBridge()
    # Convert the image message to an OpenCV image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    print(frame)
    cv.imshow("Image window", frame)
    cv.waitKey(1)


rospy.init_node('image_subscriber', anonymous=True)
sub = rospy.Subscriber('weed_detection', Image, callback)
rospy.spin()
