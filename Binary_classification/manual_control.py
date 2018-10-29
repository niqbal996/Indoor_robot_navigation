from moveRoomba import roomba_start, roomba_rotate, roomba_move, roomba_stop
from serial import Serial
import time
import cv2
import os

#TODO Not tested on PI. The RPI control part is commented out and needs to be uncommented to test on RPI.

#port = Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
file_counter = 0
frame_counter = 0
FILE_OUTPUT = 'Log_video_1.avi'
total_frame = 200

# Checks if the file exists then creates another one with higher counter.
if os.path.isfile(FILE_OUTPUT):
    file_counter += 1
    FILE_OUTPUT = 'Log_video_' + str(file_counter) + '.avi'

print ('[INFO] Press space to start Roomba')
print ('')

cap = cv2.VideoCapture(0)
# Get current width of frame
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

#Video writer
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (int(width), int(height)))


while(cap.isOpened()):
    ret, image = cap.read()

    if ret:
        frame_counter += 1
        if frame_counter > total_frames:
            break
        cv2.imshow('Current frame', image)

        #print ('Listening to Roomba control commands')
        if cv2.waitKey(1) & 0xFF == ord('w'):
            print ('Going forward')
            #roomba_move(port, 150, 300)
            time.sleep(0.2)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            print ('[INFO] Stopping the Roomba . . . ')
            #roomba_stop(port)
            time.sleep(0.2)

        if cv2.waitKey(1) & 0xFF == ord('a'):
            print ('[INFO] Stopping the Roomba to turn left now . . . .')
            #roomba_move(port, 150, 300)
            time.sleep(0.2)

        if cv2.waitKey(1) & 0xFF == ord('d'):
            print ('[INFO] Stopping the Roomba to turn right now . . . .')
            #roomba_move(port, 150, 300)
            time.sleep(0.2)

        if cv2.waitKey(1) & 0xFF == ord('\x1b'):            #Space key
            print ('[INFO] Roomba has started . . . . ')
            #roomba_start(port)
            time.sleep(0.2)

        # Saves for video
        out.write(image)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()