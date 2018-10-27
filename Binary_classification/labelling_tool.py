"""
Image labelling tool. 
author: Naeem Iqbal
email : naeemiqbal996@gmail.com
Usage:
    This program takes a video file as input and by pressing any keyboard button will mark that image as a positive and
    it into the folder provided. While pressing the mouse key will dump that image into the folder provided for negative 
    images. 
    Provide the following paths:
    Input: Path to the video file from which to crop the images
    Output: Path to the folders containing positive and negative images
    
"""
from os import path
import cv2
from matplotlib import pyplot as plt

vid = cv2.VideoCapture('test.mp4')
output_negative = '/home/shaatal/robo/Object-detection-streamer/trainer/images/door/'
output_positive = '/home/shaatal/robo/Object-detection-streamer/trainer/images/notdoor'
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

print('The video resolution is: ',height , width)
frame_number = 0
while(True):
    ret, frame = vid.read()
    frame_number = frame_number +1
    if ret==True:
        for section in range(1,5):
            section1 = frame[:,(((width / 4)*(section-1))):((width / 4)*section)]
            filename = str(section)+str(frame_number)+'.jpg'
            plt.imshow(section1)
            check = plt.waitforbuttonpress()
            if check==True:
                cv2.imwrite(path.join(output_positive , filename), section1)
                print ('Positive')
            else:
                cv2.imwrite(path.join(output_negative, filename), section1)
                print('Negative')
            continue

