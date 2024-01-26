import serial, time, string, pynmea2

port = '/dev/ttyAMA0'
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

while True:
    try:
        newdata = ser.readline().decode('utf-8')
    except:
        newdata = ser.readline().decode('utf-8')
    if newdata[0:6] == '$GPRMC':
        # print('Hello')
        msg = pynmea2.parse(newdata)
        lat = msg.latitude
        lng = msg.longitude
        gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
        print(msg)
        print(gps)

