import numpy as np
import cv2
import keyboard
from matplotlib import pyplot as plt 
from skimage.measure import compare_ssim
import time
import sys

def take_picture():
    # making sure to use the global image variable 
    global image

    # converting color output
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print("picture taken!")
    # plt.imshow(image)
    # plt.show()

def handle_inputs():
    global auto
    global key_frame

    if keyboard.is_pressed('r'):
        key_frame = gray
        print("Keyframe reset")
        time.sleep(0.4)

    if keyboard.is_pressed("q"):
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)

    if keyboard.is_pressed(" "):
        take_picture()
        time.sleep(0.4)



if __name__ == "__main__":
    # Constants
    DELTA_FREQUENCY = 60
    KEYFRAME_DELTA_SENSITIVITY = 0.82 
    MOVEMENT_SENSITIVITY = 1.91

    cap = cv2.VideoCapture(0)

    # auto-take photos
    auto = True

    # frames
    key_frame = []
    last_frame = []
    image = []
    last_delta = 0
    frame_indicator = 0
    delta = 0
    
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
            # Check if delta should be updated
            if(frame_indicator % DELTA_FREQUENCY == 0):
                # calculating the delta from the keyframe
                (new_delta, diff) = compare_ssim(key_frame, gray, full=True)
                delta = new_delta
                frame_indicator = 0
            if delta <= KEYFRAME_DELTA_SENSITIVITY:
                # if there is a previous frame and if there is not already a image
                if len(last_frame) > 0 and len(image) == 0:
                    # calculating delta value from last to current frame
                    (cur_delta, diff) = compare_ssim(gray, last_frame, full=True)
                    # if the last 2 deltas go over a threshold
                    #print(cur_delta + last_delta)   
                    if (cur_delta + last_delta) > MOVEMENT_SENSITIVITY:
                        take_picture()
                    # saving the last delta
                    last_delta = cur_delta
                # saving previous frame
                last_frame = gray
            else:
                # resetting frame values
                last_frame = []
                image = [] 
                last_delta = 0
            frame_indicator += 1

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
