import serial
import RPi.GPIO as GPIO
from subprocess import call
import os, time
from decimal import *

GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

def gps_lock():
    port.write('AT+CGPSSTATUS'+'\r\n')  # Set GPS Power ON
    rcv = port.read(10)
    print '\nwaiting for location'
    print rcv
    if rcv == 'Location 2D Fix':
        return 1;
    else:
        time.sleep(5)
        return gps_lock() 

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

if gps_lock()==1:
    port.write('AT+CGPSINF=32'+'\r\n')  # 
    rcv = port.read(10)
    print rcv
    time.sleep(1)

