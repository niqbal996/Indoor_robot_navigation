from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import cv2
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
        help="path to trained model model")
#ap.add_argument("-i", "--image", required=True,
#        help="path to input image")
args = vars(ap.parse_args())
cap = cv2.VideoCapture(0)

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])


while(True):
	# load the image
	#image = cv2.imread(args["image"])
	tic = time.time()
	ret, image = cap.read()
	orig = image.copy()

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

		# draw the label on the image
		#output = imutils.resize(orig, width=400)
		# cv2.putText(orig, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

		#Draw bounding box on the region where door(partially) is located in the image.
		print proba
		if label == 'Door' and proba > 0.70:
			cv2.rectangle(orig, (int(round((image.shape[1] / 4) * (sub_frame - 1))), 0), #top left point of the bbox
								(int(round((image.shape[1] / 4) * sub_frame)),image.shape[1]),#bottom right point of the bbox
								(0, 255, 0),										#green color of the bounding box
								3)													#line thickness of the bounding box
			cv2.putText(orig,
						str(proba),
						((20+160 * (sub_frame-1)), 30),
						 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		else:
			cv2.rectangle(orig, (int(round((image.shape[1] / 4) * (sub_frame - 1))), 0),  # top left point of the bbox
								(int(round((image.shape[1] / 4) * sub_frame)), image.shape[1]),  # bottom right point of the bbox
								(0, 0, 255),  # red color
								3)  # line thickness of the bounding box

		#print str((toc - tic)) + " Seconds"
		# show the output image
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	toc = time.time()
	cv2.putText(orig, str(1.0 / (toc - tic)) + ' FPS', (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
	cv2.imshow("Output", orig)

cap.release()