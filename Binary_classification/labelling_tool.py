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

video_name = 'Log_video_5.avi'
vid = cv2.VideoCapture(video_name)
output_negative = '..//trainer//images//notdoor//'
output_positive = '..//trainer//images//notdoor//'
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

print('The video resolution is: ',height , width)
frame_number = 0
while(True):
    vid.set(190, frame_number)            #Read the given frame number instead of reading the first frame again and again
    ret, frame = vid.read()
    frame_number = frame_number +1
    if ret==True:
        for section in range(1,5):
            section1 = frame[:,int((width / 4)*(section-1)):int((width / 4)*section)]
            filename = str(section)+'__'+video_name+'__'+str(frame_number)+'.jpg'
            plt.imshow(section1)
            check = plt.waitforbuttonpress()
            if check==True:
                cv2.imwrite(path.join(output_positive , filename), section1)
                print ('Frame number', frame_number ,'Positive')
            else:
                cv2.imwrite(path.join(output_negative, filename), section1)
                print('Frame number', frame_number ,'Negative')
            continue

