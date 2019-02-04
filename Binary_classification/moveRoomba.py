import serial
import time


def roomba_start(serialObj):
	serialObj.write(b'\x80')
	time.sleep(1)
	serialObj.write(b'\x82')
	time.sleep(1)


# for moving anything
# [137][velocity high byte][velocity low byte][radius high byte][radius low byte]
# to move straight : radius = 32768 or 0x8000
# to rotate in place : radius = 0x0001		

def roomba_rotate(serialObj,angle,velocity):
	# velocity in mm/s (v=wr, w = vr , r = 258/2 mm, so w = v*2/258) , angle specified in degrees..
	# so angle_rad = angle_deg*pi/180
	w = velocity/129.0
	time_sleep = (abs(angle)*3.14)/float(w*180)
	print (time_sleep)
	if angle > 0:
		serialObj.write(b'\x89'+chr(velocity/256)+chr(velocity%256)+b'\x00\x01')
	else:
		serialObj.write(b'\x89'+chr(velocity/256)+chr(velocity%256)+b'\xff\xff')
	time.sleep(time_sleep)
	# now stop the roomba
	serialObj.write(b'\x89\x00\x00\x00\x00')	

def roomba_move(serialObj,distance,velocity):
	# velocity in mm/s, distance in mm so time in s
	time_sleep = distance/float(abs(velocity))
	serialObj.write(b'\x89'+chr(velocity/256)+chr(velocity%256)+b'\x80\x00')
	time.sleep(time_sleep)	
	# now stop the roomba
	serialObj.write(b'\x89\x00\x00\x00\x00')	

def roomba_stop(serialObj):
	serialObj.write(b'\x89\x00\x00\x00\x00')
	serialObj.close()	



 
