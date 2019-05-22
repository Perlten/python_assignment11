import keyboard
import cv2 
import sys
import time

image = []
counter = 1000
type = "banana"


def handle_inputs():

    if keyboard.is_pressed("q"):
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)

    if keyboard.is_pressed(" "):
        take_picture()
        time.sleep(0.4)

def take_picture():
    global counter
    name = f"{type}_{counter}"
    cv2.imwrite(f"dataset5/train/{name}.jpg", image)
    print(name)
    counter += 1


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        image = frame
        cv2.imshow('frame',image)
        handle_inputs()
        cv2.waitKey(1)
    
    cap.release()
    cv2.destroyAllWindows()



    
