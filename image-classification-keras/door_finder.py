from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
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

	# pre-process the image for classification
	image = cv2.resize(image, (28, 28))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)


	# classify the input image
	(notSanta, santa) = model.predict(image)[0]

	# build the label
	label = "Santa" if santa > notSanta else "Not Santa"
	proba = santa if santa > notSanta else notSanta
	label = "{}: {:.2f}%".format(label, proba * 100)

	# draw the label on the image
	#output = imutils.resize(orig, width=400)
	cv2.putText(orig, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
	toc = time.time()
	cv2.putText(orig, str(1.0/(toc-tic))+' FPS', (10, 45),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
	#print str((toc - tic)) + " Seconds"
	# show the output image
	cv2.imshow("Output", orig)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
