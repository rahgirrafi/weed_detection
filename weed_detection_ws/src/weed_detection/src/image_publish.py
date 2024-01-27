#!/usr/bin/env python3

import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

gps =  ''
def callback(data):
    global gps
    gps = data.data   

def object_detector():


    bridge = CvBridge()
    cap = cv.VideoCapture(-1)
    rospy.init_node('image_publish', anonymous=True)
    bbox_pub = rospy.Publisher('weed_detection', Image, queue_size=10)
    gps_sub = rospy.Subscriber('gps', String, callback)
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        # Read a frame from the camera
        
        ret, frame = cap.read()

        if ret:
            ros_img = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
            #put gps data on image
            ros_img = cv.putText(frame, gps, (0,25), cv.FONT_HERSHEY_COMPLEX, 0.5 , (0,255,255), 1, cv.LINE_AA)
            # Publish the image
            bbox_pub.publish(ros_img)
            rate.sleep()
    cap.release()

if __name__ == '__main__':
    try:
        object_detector()
    except rospy.ROSInterruptException:
        pass
