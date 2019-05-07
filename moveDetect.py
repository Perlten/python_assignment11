import numpy as np
import cv2
import keyboard
from matplotlib import pyplot as plt 
from skimage.measure import compare_ssim
import time
import sys

def take_picture():
    # making sure to use the global caption variable 
    global caption

    # converting color output
    caption = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print("picture taken!")
    plt.imshow(caption)
    plt.show()

def handle_inputs():
    global auto
    global key_frame

    if keyboard.is_pressed('a'):
        auto = not auto
        
        if auto:
            print("AUTO - activated")
            key_frame = gray
            print("key_frame reset")
        else:
            print("AUTO - deactivated")
        time.sleep(0.3)

    if keyboard.is_pressed("q"):
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)

    if keyboard.is_pressed(" "):
        take_picture()
        time.sleep(0.4)


cap = cv2.VideoCapture(0)

# auto-take photos
auto = False

# frames
key_frame = []
last_frame = []
caption = []
last_delta = 0

while True:
    # get frame
    ret, frame = cap.read()
    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if len(key_frame) == 0:
        key_frame = gray

    cv2.imshow('frame',frame)

    handle_inputs()

    # if we have auto enabled
    if auto:
        # calculating the delta from the keyframe
        (delta, diff) = compare_ssim(key_frame, gray, full=True)
        if delta <= 0.82:
            # if there is not already a caption
            # print(caption)
            if len(caption) == 0:
                # if there is a previous frame
                if len(last_frame) > 0:
                    # calculating delta value from last to current frame
                    (cur_delta, diff) = compare_ssim(gray, last_frame, full=True)
                    # if the last 2 deltas go over a threshold
                    if last_delta > 0 and (cur_delta + last_delta) > 1.69:
                        take_picture()
                    # saving the last delta
                    last_delta = cur_delta
                # saving previous frame
                last_frame = gray
        else:
            # resetting frame values
            last_frame = []
            caption = [] 
            last_delta = 0

    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
