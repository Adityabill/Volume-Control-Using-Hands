import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htr
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

width_cam, height_cam = 1000, 1000 #height and width of the output screen

capture = cv2.VideoCapture(0) #Selection of camera (0 for device webcam)
capture.set(3, width_cam)
capture.set(4, height_cam)

prev_time = 0
curr_time = 0

detector = htr.handDetector(detectionCon=0.72) #creating object from hand detector module

#Setting volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()

min_volume = volume_range[0]
max_volume = volume_range[1]
vol = 0
volume_bar = 400
vol_per = 0

while True:
    success, img = capture.read()
    img=detector.find_hands(img)
    landmark_list = detector.find_pos(img, draw=False)
    if len(landmark_list)!=0:
        print(landmark_list[4], landmark_list[8])
        x1, y1=landmark_list[4][1], landmark_list[4][2] #coordinates of thumb
        x2, y2=landmark_list[8][1], landmark_list[8][2] #coordinates of index finger
        center_x, center_y = (x1+x2)//2, (y1+y2)//2 #coordinates of center of line between the 2 fingers
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) #circle on thumb
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED) #circle on index finger
        cv2.line(img, (x1, y1), (x2, y2), (0, 180, 34), 3) #line between the 2 fingers
        cv2.circle(img, (center_x, center_y), 15, (255, 0, 255), cv2.FILLED) #circle in the line between the 2 fingers
        length = math.hypot(x2-x1, y2-y1)
        print(length)

        vol = np.interp(length, [50, 300], [min_volume, max_volume]) #volume value
        volume_bar = np.interp(length, [50, 300], [400, 150]) #volume bar value
        vol_per = np.interp(length, [50, 300], [0, 100]) #volume percent value
        print(vol)
        volume.SetMasterVolumeLevel(vol, None) #setting volume as per vol variable

        if length<50: # circle in the line between the 2 fingers when distance between the two fingers is less than 50
            cv2.circle(img, (center_x, center_y), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volume_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{str(int(vol_per))}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 204), 3)

    curr_time = time.time()
    fps = 1/(curr_time-prev_time) #calculation of fps
    prev_time=curr_time

    cv2.putText(img, f'FPS: {str(int(fps))}', (10, 65), cv2.FONT_HERSHEY_PLAIN, 2, (100, 72, 164), 3) #FPS text on the output screen
    cv2.imshow("Video Capure", img) #Output screen
    cv2.waitKey(1)
