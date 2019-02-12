'''
This script takes in the images dataset and generates a binary classifier neural network which
can be used by the door_scanner.py script to detect doors.
Dataset:
	The images should be in /images/door and /image/notdoor folder
Usage:
	python train_network.py --dataset images --model model_name.model
Arguments:
	--dataset or -d:  the folder which contains the images to be used for the training and validation
	--model or -m: The name of the output model to be generated

NOTE: if the image names have spaces in the them then this script throws an error. In order to deal with that,
use sort_dataset.py before running the training script.
'''

# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from pyimagesearch.lenet import LeNet
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os


def plot_history(history):
	loss_list = [s for s in history.history.keys() if 'loss' in s and 'val' not in s]
	val_loss_list = [s for s in history.history.keys() if 'loss' in s and 'val' in s]
	acc_list = [s for s in history.history.keys() if 'acc' in s and 'val' not in s]
	val_acc_list = [s for s in history.history.keys() if 'acc' in s and 'val' in s]

	if len(loss_list) == 0:
		print('Loss is missing in history')
		return

	## As loss always exists
	epochs = range(1, len(history.history[loss_list[0]]) + 1)

	## Loss
	plt.figure(1)
	for l in loss_list:
		plt.plot(epochs, history.history[l], 'b',
				 label='Training loss (' + str(str(format(history.history[l][-1], '.5f')) + ')'))
	for l in val_loss_list:
		plt.plot(epochs, history.history[l], 'g',
				 label='Validation loss (' + str(str(format(history.history[l][-1], '.5f')) + ')'))

	plt.title('Loss')
	plt.xlabel('Epochs')
	plt.ylabel('Loss')
	plt.legend()

	## Accuracy
	plt.figure(2)
	for l in acc_list:
		plt.plot(epochs, history.history[l], 'b',
				 label='Training accuracy (' + str(format(history.history[l][-1], '.5f')) + ')')
	for l in val_acc_list:
		plt.plot(epochs, history.history[l], 'g',
				 label='Validation accuracy (' + str(format(history.history[l][-1], '.5f')) + ')')

	plt.title('Accuracy')
	plt.xlabel('Epochs')
	plt.ylabel('Accuracy')
	plt.legend()
	plt.show()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output loss/accuracy plot")
args = vars(ap.parse_args())

# initialize the number of epochs to train for, initia learning rate,
# and batch size
EPOCHS = 25
INIT_LR = 1e-3
BS = 32

# initialize the data and labels
print("[INFO] loading images...")
data = []
labels = []

# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# loop over the input images
for imagePath in imagePaths:
	# load the image, pre-process it, and store it in the data list
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (28, 28))
	image = img_to_array(image)
	data.append(image)

	# extract the class label from the image path and update the
	# labels list
	label = imagePath.split(os.path.sep)[-2]
	label = 1 if label == "door" else 0
	labels.append(label)

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.25, random_state=42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=2)
testY = to_categorical(testY, num_classes=2)

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=28, height=28, depth=3, classes=2)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS, verbose=0)

plot_history(H)

# save the model to disk
print("[INFO] serializing network...")
model.save(args["model"])

#plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on door/Not door")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])