import numpy as np
import cv2
import keyboard
from matplotlib import pyplot as plt 
from skimage.measure import compare_ssim
import time
import sys
import copy
import webbrowser
from fruitDetect import detect_fruit
# from multiprocessing import Process

from PIL import ImageFont, ImageDraw, Image

def take_picture():
    # making sure to use the global image variable 
    global image

    # converting color output
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print("picture taken!")
    return image

def predict_picture():
    global type_found, time_found, found_confirmed

    picture_taken = take_picture()
    type_found = detect_fruit(image)
    time_found = time.time()
    found_confirmed = False

def handle_inputs():
    global auto, key_frame, found_confirmed, time_found, type_found, selected, prices

    if keyboard.is_pressed('r'):
        key_frame = gray
        print("Keyframe reset")
        time.sleep(0.4)

    if keyboard.is_pressed("q"):
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)

    if keyboard.is_pressed(" "):
        predict_picture()
        time.sleep(0.4)

    if keyboard.is_pressed("y"):
        if type_found:
            found_confirmed = True
            time_found = None


    if keyboard.is_pressed("n"):
        type_found = None
        found_confirmed = False
        time_found = None

    if len(prices) > 0:
        if keyboard.is_pressed("up"):
            selected -= 1
            if selected < 0:
                selected = 0

        if keyboard.is_pressed("down"):
            selected += 1
            if selected > (len(prices) - 1):
                selected = (len(prices) - 1)
        
        if keyboard.is_pressed("enter"):
            if 2 < len(prices[selected]):
                webbrowser.open(prices[selected][2])
            
            

def display_content():
    global frame, f_width, f_height, type_found, prices, found_confirmed, label_height, label_width, time_found, selected
    
    # copying frame
    dframe = copy.copy(frame)

    font = cv2.FONT_HERSHEY_COMPLEX

    if not found_confirmed: 
        if time_found:
            # Calculate time remaining for countdown
            counter = int((time_found + 5) - time.time())
            
            # If it goes under zero, accept the type found
            if counter < 0:
                found_confirmed = True
                time_found = None
            # If not, display the counter
            else:
                cv2.putText(dframe, str(counter), (int(f_width / 2) - 40,100), font, 4, (255,255,255), 5, cv2.LINE_AA)

    
    if type_found:
        # Generate type text depending on confirmation
        display_found = type_found
        indent = 80
        if not found_confirmed:
            display_found = f"Is this: {type_found}?"
            indent = 180

        # Displaying type text 
        cv2.putText(dframe, display_found, (int(f_width/2) - indent, (f_height-30)), font, 1.5, (255,255,255), 5, cv2.LINE_AA)

    # Value for relative height position 
    height_pos = 0
    for key, price in enumerate(prices):
        # If the current price is the selected one, display the background color as white
        label_color = (0,255,255)
        if key == selected:
            label_color = (255,255,255)
        
        # Draw background
        cv2.rectangle(dframe, (10,10 + height_pos), (200,label_height + 10 + height_pos), label_color, -1)

        # Display store
        cv2.putText(dframe, price[1], (15,25 + height_pos), font, 0.4, (0,0,0), 1, cv2.LINE_AA)

        # Display price
        cv2.putText(dframe, f"{price[0]} kr", (15,60 + height_pos), font, 1, (0,0,0), 1, cv2.LINE_AA)

        if 2 < len(price):
            # Display price
            cv2.putText(dframe, ">", (label_width + 70, int(label_height / 2) + 20 + height_pos), font, 0.7, (0,0,0), 1, cv2.LINE_AA)

        # Append height_pos
        height_pos += label_height + 10

    return dframe

if __name__ == "__main__":
    # Constants
    DELTA_FREQUENCY = 30
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

    # displays
    type_found = "apple"
    time_found = time.time()
    found_confirmed = False
    prices = [(3,"Kwickly", "https://kwickly.dk/"), (4, "Netto"), (6, "Irma", "https://irma.dk/"), (2,"Fakta", "https://fakta.dk/")]

    # selection
    selected = 0
    
    # p = Process(target=handle_inputs)
    # p.start()
    
    while True:
        # get frame
        ret, frame = cap.read()

        frame = cv2.resize(frame, (640,480))
        # convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # first frame
        if len(key_frame) == 0:
            key_frame = gray
            
            # helpers
            f_width = frame.shape[1]
            f_height = frame.shape[0]
            label_height = int(f_height/8)
            label_width = int(f_width/6)
            print("resolution: ", time_found)

        dframe = display_content()

        cv2.imshow('frame',dframe)

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
                    print(cur_delta + last_delta)   
                    # if the last 2 deltas go over a threshold
                    if (cur_delta + last_delta) > MOVEMENT_SENSITIVITY:
                        predict_picture()
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

    # p.join()
    cap.release()
    cv2.destroyAllWindows()
