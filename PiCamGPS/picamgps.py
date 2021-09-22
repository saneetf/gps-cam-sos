import serial
import datetime
import RPi.GPIO as GPIO
from subprocess import call
import os, time
from decimal import *

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP) # set the GPIO pin for the capture photo push button
port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)

file
argument = "raspistill -o photo"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".jpg" # command to take photo
filename = "photo.jpg"

def modem_init():
	"Initialize Modem"
	

	port.write('AT'+'\r\n')
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	port.write('ATE0'+'\r\n')      # Disable the Echo
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	port.write('AT+CGPSPWR=1'+'\r\n')  # Set GPS Power ON
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	return;
def modem_send(lat1,lon1):
	# Transmitting AT Commands to the Modem
	# '\r\n' indicates the Enter key
	port.write('AT'+'\r\n')
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	port.write('ATE0'+'\r\n')      # Disable the Echo
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	# Sending a message to a particular Number
        # 9921934621
        # 9130443830
        # 7030467082
        
	port.write('AT+CMGS="9921934621"'+'\r\n') # put recipient number here
	rcv = port.read(10)
	print rcv
	time.sleep(1)

	port.write('PiCam Location Update:('+str(lat1)+','+str(lon1)+')'+'\nhttps://maps.google.com/?q='+str(lat1)+','+str(lon1)+'\r\n')  # Message
	rcv = port.read(10)
	print rcv

	port.write("\x1A") # Enable to send SMS for i in range(10):
	rcv = port.read(10)
	print rcv

	return;

def find(str, ch):
	for i, ltr in enumerate(str):
		if ltr == ch:
			yield i

def modem_getloc_send():

	port.write('AT+CGPSINF=32'+'\r\n')   # New SMS Message Indications
	time.sleep(1)
	data = port.read(100)
	print data
	gpsmsg=data.split(',')
	lat=gpsmsg[3]
	lon=gpsmsg[5]

	s1=lat[2:len(lat)]
	s1=Decimal(s1)
	s1=s1/60
	s11=int(lat[0:2])
	s1=s11+s1

	s2=lon[3:len(lon)]
	s2=Decimal(s2)
	s2=s2/60
	s22=int(lon[0:3])
	s2=s22+s2

	print s1
	print s2
	time.sleep(1)

	modem_send(s1,s2)
	return;

def init():
	"Run Initialization Code Once"
	modem_init()
	return;
def loop():
	"Run Main Process"
	while True:

		if(GPIO.input(13) ==0): # condition for capture photo push button to be activated
			time.sleep(0.25) #
			call ([argument], shell = True) # call the "raspistill" bash command
			modem_getloc_send()
			time.sleep(2) # leave for 2 seconds
	GPIO.cleanup()
	return;

init()
loop()
