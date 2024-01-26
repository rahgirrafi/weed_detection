#!/usr/bin/env python3
import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch

#from RPi import GPIO #uncomment only for raspberry pi
#import time #uncomment only for raspberry pi
'''
def setup_LED():
    GPIO.setmode(GPIO.BCM) #uncomment only for raspberry pi
    gpio_pin = 17  # Replace with the actual GPIO pin number
    GPIO.setup(gpio_pin, GPIO.OUT)

def_LED_blink():
    GPIO.output(gpio_pin, GPIO.HIGH)
'''

def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path="/media/rafi/Technical/Projects/weed_detection/weed_detection_ws/src/weed_detection/src/custom3.pt", force_reload= True)
    return model

model = load_model()

def callback(data):
    bridge = CvBridge()
    # Convert the image message to an OpenCV image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    #print(frame)
    results = model(frame)
    #get the prediction class
    try:
        prediction = results.xyxy[0].numpy()[0,5]
        print(prediction)
    except:
        pass
    cv.imshow("Image window", results.render()[0])
    cv.waitKey(1)


rospy.init_node('image_process_subscribe', anonymous=True)
sub = rospy.Subscriber('weed_detection', Image, callback)
rospy.spin()
