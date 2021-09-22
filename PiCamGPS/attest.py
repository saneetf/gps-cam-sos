import serial   
import os, time
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyUSB0", baudrate=4800, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
 
port.write('AT'+'\r\n')
print 'sent'
time.sleep(1)
port.write('AT+CGPSPWR=1'+'\r\n')
rcv = port.read()
print 'recvd'
print rcv
