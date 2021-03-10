#!/usr/bin/env python3
import cv2
import time
import random
import numpy

from mss import mss
from PIL import Image
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from config import MONITOR, KEY_SIZE, KEY_PADDING, THRESHOLD

random = random.Random()

keyboard = KeyboardController()
mouse = MouseController()
sct = mss()

keys = {
    "e": cv2.imread("frame_e.png"),
    "q": cv2.imread("frame_q.png")
} 


def detect_key(frame):
    for key, image in keys.items():
        result = cv2.matchTemplate(frame, image, cv2.TM_CCOEFF_NORMED)[0][0]
        print("Checking key " + key.upper() + ", result: " + str(result))

        # If result is above threshold, it's a match
        if result > THRESHOLD:
            return key

    return None


def main():
    print("4Life Kopalnia boteł, made by xDDD w Pytongu przy użyciu opencv, mss i pynput")
    time.sleep(1)

    # Current key and retries
    n, retry = 0, 0

    while True:
        frame = sct.grab(MONITOR)

        # Create an Image
        img = Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX")
        pixels = img.load()

        # Crop image to the key we are currently looking for
        key_frame = img.crop((n * (KEY_SIZE + KEY_PADDING), 0, (n * (KEY_SIZE + KEY_PADDING)) + KEY_SIZE, KEY_SIZE))

        # Convert frame to opencv format
        open_cv_image = numpy.array(key_frame)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        print("-- KEY: " + str(n) + ", retry: " + str(retry))
        result = detect_key(open_cv_image)
        
        if result:
            keyboard.press(result)
            keyboard.release(result)
        elif retry == 1:            
            # Wait 0.5 second before we can continue
            time.sleep(0.5)
            n, retry = 0, 0
            
            mouse.press(Button.left)
            mouse.release(Button.left)
            continue
        else:
            time.sleep(0.1)
            retry = 1

            print("Retrying...")
            continue

        # Increase key to check for next frame
        n += 1
        retry = 0

        # Randomize sleep to imitate human behaviour
        delay = random.randint(15, 30) / 100

        print("Sleeping for " + str(delay) + "ms...")
        time.sleep(delay)

        if n == 3:
            # Wait 3 seconds before we can continue
            time.sleep(3)
            n, retry = 0, 0
            
            mouse.press(Button.left)
            mouse.release(Button.left)


if __name__ == "__main__":
    main()
