#!/usr/bin/env python3

import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

gps =  ''
latitude = 0
longitude = 0
text = ''
def callback(data):
    global gps , latitude, longitude, text
    gps = data.data
    latitude = gps.split(',')[1]
    longitude = gps.split(',')[2]
    text = 'Latitude: ' + latitude + ' Longitude: ' + longitude

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
            #put gps data on image
            ros_img = cv.putText(frame, text, (0,25), cv.FONT_HERSHEY_COMPLEX, 0.5 , (0,255,255), 1, cv.LINE_AA)
            ros_img = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
            # Publish the image
            
            bbox_pub.publish(ros_img)
            rate.sleep()
    cap.release()

if __name__ == '__main__':
    try:
        object_detector()
    except rospy.ROSInterruptException:
        pass
