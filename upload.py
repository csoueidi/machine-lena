import urllib, json
import requests

from picamera import PiCamera
from time import sleep
from pygame import mixer
import RPi.GPIO as GPIO


camera = PiCamera()

GPIO.setmode(GPIO.BCM)
allPins=[12,18,23,24,25]

for pin in allPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)


currentEmotions = []


while True:
    try:
        sleep(1)
        currentEmotions = []
        
        camera.resolution = (1216, 912)
        #camera.resolution = (640, 480)
        camera.start_preview()
        sleep(1)
        camera.capture('/home/pi/Desktop/image.jpg')
        camera.stop_preview()
        print("Took pic")
    except:
        print("Error")
    
 
