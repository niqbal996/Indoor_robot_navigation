'''A helper class to maneuver roomba robot according to the parameters given
parameters:
    Speed:      integer number in mm/s +ve or -ve

'''
radius = 30
import serial.tools.list_ports
import time
elocity = 200 #in mm/s
ports=serial.tools.list_ports.comports()
print("Ports: ", ports)
#open Raspi GPIO serial port, speed 115200 for Roomba 5xx
ser = serial.Serial('/dev/ttyAMA0',115200)

#ser = serial.Serial('/dev/ttyAMA0',57600)  # open Raspi GPIO serial port, speed 57600 for Roomba 3xx
print(ser.name)         # check which port was really used


#Start mode the Roomba
ser.write(b'\x80')
time.sleep(1)

#Control mode:
ser.write(b'\x82')
time.sleep(2)

# Vacuum motors on:
ser.write(b'\x8a\x07')
time.sleep(0.2)

# go forward
# ser.write(b'\x89\x00\xfa'+chr(radius/256)+chr(radius%256))
# slower:
ser.write(b'\x89\x00\x80' + chr(radius / 256) + chr(radius % 256))