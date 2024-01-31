#!/usr/bin/env python3
from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)

gpio_pin = 17  # Replace with the actual GPIO pin number

GPIO.setup(gpio_pin, GPIO.OUT)

GPIO.output(gpio_pin, GPIO.HIGH)

time.sleep(5)

GPIO.cleanup()

