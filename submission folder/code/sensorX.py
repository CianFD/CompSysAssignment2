
import RPi.GPIO as GPIO #imports GPIO Section of RPi Package and labels it GPIO
from picamera import PiCamera #imports PiCamera section of picamera package
import time #imports time package
import datetime #imports datetime package
import storeFileFB #imports storeFileFB.py script from same folder
from gpiozero import TonalBuzzer #imports TonalBuzzer Section of GPIOZero Package
from gpiozero.tones import Tone #imports  Tone Section of GPIOZero.tones Package
from urllib.request import urlopen
import json

sensor = 25 #labels input from GPIOPin 25, which is connected to the Funduino Sound Detection Sensor as sensor
buzzer = TonalBuzzer(23) #labels input from GPIOPin 23 which is connected to the Keyesudio Passive Buzzer as buzzer and assigns it to the TonalBuzzer classification
camera = PiCamera() #labels input from the PiCamera(RPi Camera Module V2) as camera

GPIO.setmode(GPIO.BCM) #sets GPIO mode as BCM  to take in the Broadcom Input Values so it listens to the right Pins
GPIO.setup(sensor, GPIO.IN) #sets sensor as a GPIO Input Device to take in information from it

WRITE_API_KEY='S7ESRFX5NJU6NMNM' #taken from ThingSpeak Channel to allow input from Sensor to be sent to ThingSpeak
baseURL='https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY #ThingSpeak Channel URL to be used when submitting information to ThingSpeak Channel which will then trigger the ThingTweet React

SNDdetected = 0 #sets SNDdetected value as 0
camera.start_preview() #triggers camera into a ready state
frame = 1 #sets value of frame as 1
fileLoc = f'/home/pi/project2/cameraimages/frame{frame}.jpg' #sets the folder location of where the images captured will be stored
currentTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") #uses datetime library to set value of current time as date and time in the format dd/mm/yyyy hh:mm:ss

def SNDEventHandler(sensor): #creates the SNDEventHandler method which takes in the value of sensor
	print ("Sound Detected!") #prints message to the console
	SNDdetected = 1 #sets SNDdetected value to 1
	buzzer.play(Tone(note='A5')) #sends message to the passive buzzer to play note A5
	if (SNDdetected == 1): #if a sound is detected
		camera.capture(fileLoc) #camera takes a photo and saves the image to the fileLoc folder defined above
		storeFileFB.store_file(fileLoc) #triggers store_file method from storeFileFB script using value of fileLoc which stores the captured image in firebase storage
		storeFileFB.push_db(fileLoc, currentTime)  #triggers push_db method from storeFileFB script using value of fileLoc and current time which pushes the captured image to the firebase realtime database 
	time.sleep(5) #sleep for 5 seconds while buzzer is ringing away
	buzzer.stop() #stops the buzzer
	conn = urlopen(baseURL + '&field1=%s' % (SNDdetected)) #triggers a URL using the Thingspeak URL above which reads in the new value of SNDdetected triggering the ThingTweet to be posted.
	print(conn.read()) #information is printed to the URL thus triggering the ThingTweet
	conn.close() #temp connection to trigger URL is then closed


GPIO.add_event_detect(sensor, GPIO.BOTH, callback=SNDEventHandler, bouncetime=2000) #creates a detect event which takes in value of sensor, detects both rising and falling callbacks, takes in the SNDEventHandler as a callback method, and adds a bouncetime of 2000ms


while True: #sets the script to go on for an infinite loop which has a sleep time of 10 seconds so it's consistently listening
	time.sleep(10)
	frame +=1 #adds 1 to the value of frame so the next frame saved will be 2, then 3 and so on.
