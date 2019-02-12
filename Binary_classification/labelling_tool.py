"""
Image labelling tool. 
author: Naeem Iqbal
email : naeemiqbal996@gmail.com
Usage:
    This program takes a video file as input and generates four sub frames from each frame and put them into the door
    folder. After that you have to manually seperate door or not door images.
Provide the following paths:
    Input: Path to the video file from which to crop the images
    Output: Path to the folders containing positive and negative images

TODO:
    Add a button functionality at the time of displaying images and depending on which button was pressed decided
    whether the sub image has a door in it or not. Not sure if it will speed up the labelling process but it will be
    less prone to bad/wrong samples.
"""
from os import path
import cv2
from matplotlib import pyplot as plt

video_name = 'Log_video_office_oleg_7.avi'
vid = cv2.VideoCapture(video_name)
output_negative = '..//trainer//images//notdoor//'
output_positive = '..//trainer//images//notdoor//'
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

print('The video resolution is: ',height , width)
frame_number = 0
amount_of_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
while(True):
    vid.set(1, frame_number)            #Read the given frame number instead of reading the first frame again and again
    ret, frame = vid.read()
    frame_number = frame_number +1
    if ret==True and (frame_number <= amount_of_frames):
        for section in range(1,5):
            section1 = frame[:,int((width / 4)*(section-1)):int((width / 4)*section)]
            filename = str(section)+'__'+video_name+'__'+str(frame_number)+'.jpg'
            #plt.imshow(section1)
            #check = plt.waitforbuttonpress()
            # if check==True:
            cv2.imwrite(path.join(output_positive , filename), section1)
            print ('Frame number', frame_number ,'Positive')
            # else:
            #     cv2.imwrite(path.join(output_negative, filename), section1)
            #     print('Frame number', frame_number ,'Negative')
            continue

    if frame_number == amount_of_frames-1:
        print("[INFO] Video Completed ....")
        break


