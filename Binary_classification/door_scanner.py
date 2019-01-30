from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import cv2
import time
import serial.tools.list_ports


ports=serial.tools.list_ports.comports()
print("Ports: ", ports)
# open Raspi GPIO serial port, speed 115200 for Roomba 5xx
# ser = serial.Serial('/dev/ttyAMA0',115200)
#
# #ser = serial.Serial('/dev/ttyAMA0',57600)  # open Raspi GPIO serial port, speed 57600 for Roomba 3xx
# print(ser.name)         # check which port was really used

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
        help="path to trained model model")
#ap.add_argument("-i", "--image", required=True,
#        help="path to input image")
args = vars(ap.parse_args())
#cap = cv2.VideoCapture(0)       			#Feed from camera
cap = cv2.VideoCapture('Log_video_1.avi')	#Feed from video recording

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])

# #Start mode the Roomba
# ser.write(b'\x80')
# time.sleep(1)
#
# #Control mode:
# ser.write(b'\x82')
# time.sleep(2)
#
# # Vacuum motors on:
# ser.write(b'\x8a\x07')
# time.sleep(0.2)

position_vector = [0, 0, 0, 0]
while(True):
	tic = time.time()
	ret, image = cap.read()
	if ret ==  False: #GET OUT
		break
	orig = image.copy()

	# Reset the position vector for each frame
	position_vector = [0, 0, 0, 0]
	#Scan the room rotate in steps very slowly
	rn = np.random.random(1)
	#print("nr =", rn)
	radius =  30 #int((rn[0] - 0.5) * 4000.0)     # rotate 30 degree in each step and then scan the images.
	# if radius < 0:
	# 	radius += 2 ** 16 - 1
	#print("Radius= ", radius)
	# go forward
	# ser.write(b'\x89\x00\xfa'+chr(radius/256)+chr(radius%256))
	# slower:
	#ser.write(b'\x89\x00\x80' + chr(radius / 256) + chr(radius % 256))
	#print ('[INFO] Turning and scanning now . . . ')
	for sub_frame in range(1, 5):
		#Extract the subsection of the image.
		left = int(round((image.shape[0] / 4) * (sub_frame - 1)))
		right= int(round((image.shape[1] / 4) * sub_frame))
		section = image[:, int(round((image.shape[0] / 4) * (sub_frame - 1))):int(round((image.shape[0] / 4) * sub_frame))]

		# pre-process the image for classification
		section = cv2.resize(section, (28, 28))
		section = section.astype("float") / 255.0
		section = img_to_array(section)
		section = np.expand_dims(section, axis=0)

		# classify the input image
		(notDoor, door) = model.predict(section)[0]

		# build the label
		label = "Door" if door > notDoor else "Not Door"
		proba = door if door > notDoor else notDoor
		label_with_proba = "{}: {:.2f}%".format(label, proba * 100)

		#Draw bounding box on the region where door(partially) is located in the image.
		if label == 'Door':
			#Change the status of position vector depending on which sub section of the image it is.
			position_vector[sub_frame-1] = 1

			#Draw green rectangle
			cv2.rectangle(orig, (int(round((image.shape[1] / 4) * (sub_frame - 1))), 0), #top left point of the bbox
								(int(round((image.shape[1] / 4) * sub_frame)),image.shape[1]),#bottom right point of the bbox
								(0, 255, 0),										#green color of the bounding box
								3)													#line thickness of the bounding box

			#Write the probability of Door occurence.
			cv2.putText(orig,
						str(proba),
						((20+160 * (sub_frame-1)), 30),
						 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		else:
			cv2.rectangle(orig, (int(round((image.shape[1] / 4) * (sub_frame - 1))), 0),  # top left point of the bbox
								(int(round((image.shape[1] / 4) * sub_frame)), image.shape[1]),  # bottom right point of the bbox
								(0, 0, 255),  # red color
								3)  # line thickness of the bounding box

		# show the output image
		toc = time.time()
	#If two center values are 1 then stop the scanning phase.
	#Go straight
	if position_vector[1] == 1  and position_vector[2] == 1:
		# Move towards the door slowly
		print('[INFO] Moving forward . . .')
		# ser.write(b'\x89\x00\x80\x80\x00')
	# Turn left
	elif (position_vector[2] == 1  and position_vector[3] == 1) or (position_vector[3]):
		print ('[INFO] Turning left 30 degrees now')
		# ser.write(b'\x89\x00\x80\x80\x00')
	#Turn right
	elif (position_vector[2] == 0  and position_vector[1] == 1) or (position_vector[0]):
		print ('[INFO] Turning right 30 degrees now')
		# ser.write(b'\x89\x00\x80\x80\x00')
	else:
		print('[INFO] Continue scanning for door frames . . .')

	cv2.putText(orig, str(1.0 / (toc - tic)) + ' FPS', (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
	cv2.imshow("Output", orig)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#stop,speed 0:
# ser.write(b'\x89\x00\x00\x00\x00')
# time.sleep(0.2)
# #vacuum motors off:
# ser.write(b'\x8a\x00')
# time.sleep(0.2)
# print("close")
# ser.close()

# When everything done, release the capture
cap.release()

