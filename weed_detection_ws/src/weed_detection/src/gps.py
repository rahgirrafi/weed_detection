#!/usr/bin/env python3

import serial, time, string, pynmea2
import rospy
from std_msgs.msg import String

def start_gps():

    port = '/dev/ttyAMA0'
    ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    rospy.init_node('gps', anonymous=True)
    pub = rospy.Publisher('gps', String, queue_size=10)
    rate = rospy.Rate(30)   

    while not rospy.is_shutdown():
        try:
            newdata = ser.readline().decode('utf-8')
        except:
            newdata = ser.readline().decode('utf-8')
        if newdata[0:6] == '$GPRMC':
            # print('Hello')
            msg = pynmea2.parse(newdata)
            lat = msg.latitude
            lng = msg.longitude
            gps = "Latitude = " + str(lat) + " Longitude = " + str(lng)
            #print(msg)
            pub.publish(gps)
            print(gps)


if __name__ == '__main__':
    try:
        start_gps()
    except rospy.ROSInterruptException:
        pass