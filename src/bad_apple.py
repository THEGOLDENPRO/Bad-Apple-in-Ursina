import cv2
import time
import sys
from PIL import Image, ImageColor

bad_apple_cap = cv2.VideoCapture("./bad_apple.mp4")

frame = bad_apple_cap.read()[1]

while(bad_apple_cap.isOpened()):
    frame = bad_apple_cap.read()[1]

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
