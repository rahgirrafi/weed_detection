#!/usr/bin/env python3

import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def object_detector():
    bridge = CvBridge()
    cap = cv.VideoCapture(-1)
    rospy.init_node('image_publish', anonymous=True)
    bbox_pub = rospy.Publisher('weed_detection', Image, queue_size=10)

    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        # Read a frame from the camera
        ret, frame = cap.read()
        if ret:
            ros_img = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
            # Publish the image
            bbox_pub.publish(ros_img)
            print('Published')
            rate.sleep()

    # Release the video capture object when the node is terminated
    cap.release()

if __name__ == '__main__':
    try:
        object_detector()
    except rospy.ROSInterruptException:
        pass

    #ok
