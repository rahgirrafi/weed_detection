#!/usr/bin/env python3
import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch
import os
from std_msgs.msg import String
import csv

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
model_path = '/home/sharnali' + '/weed_detection/weed_detection_ws/src/weed_detection/src/custom3.pt'
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path= model_path, force_reload= True)
    return model

model = load_model()

gps =  ''
latitude = ''
longitude = ''
text = ''
time = ''
def callback2(data):
    global gps, latitude, longitude, time
    gps = data.data
    time = gps.split(',')[0]
    latitude = gps.split(',')[0]
    longitude = gps.split(',')[1]

def callback(data):
    bridge = CvBridge()
    # Convert the image message to an OpenCV image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    #print(frame)
    results = model(frame)
    #get the prediction class
    try:
        prediction = results.xyxy[0].numpy()[0,5]
        if int(prediction) == 0:
            with open('/home/sharnali/Desktop/record.csv', 'a') as file:
                writer = csv.writer(file)
                if os.stat('/home/sharnali/Desktop/record.csv').st_size == 0:
                    writer.writerow(['Time','Longitude', 'Latitude'])    
                writer.writerow([time, longitude, latitude])
            
    except:
        pass
    cv.imshow("Image window", results.render()[0])
    cv.waitKey(1)



rospy.init_node('image_process_subscribe', anonymous=True)
sub = rospy.Subscriber('weed_detection', Image, callback)
gps_sub = rospy.Subscriber('gps', String, callback2)

rospy.spin()
