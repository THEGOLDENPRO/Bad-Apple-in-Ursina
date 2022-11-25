import sys
import threading
import cv2
from typing import Dict
from ursina import Ursina, Entity, Vec3, Vec2, camera, Keys, held_keys, color, time, window, mouse, clamp, destroy, Audio
from ursina.prefabs.first_person_controller import FirstPersonController

window.borderless = False

blocks:Dict[Vec3, Entity] = {}

class UwUCamera(Entity):
    def __init__(self):
        super().__init__()

        self.controller = FirstPersonController()
        self.controller.gravity = 0
        self.controller.speed = 8
        self.controller.cursor.disable()

        self.controller.position = Vec3(0, 22, 0)

    def update(self):
        if held_keys["space"]:
            self.controller.position += (self.controller.up * 8) * time.dt

        if held_keys[Keys.left_shift]:
            self.controller.position += (self.controller.down * 8) * time.dt

        if held_keys[Keys.escape]:
            sys.exit(0)


class Block(Entity):
    def __init__(self, location:Vec3):
        super().__init__()

        blocks[location] = self

        self.model = "cube"
        self.position = location
        #self.collider = "box"

def start():
    app = Ursina()

    UwUCamera()
    
    bad_apple_cap = cv2.VideoCapture("./output_64x48.mp4")

    # Get first frame.
    frame = bad_apple_cap.read()[1]

    # Grab the image dimensions.
    height = frame.shape[0]; width = frame.shape[1]

    for y in range(0, height):
        for x in range(0, width):
            Block(location=Vec3(x,0,y))

    while bad_apple_cap.isOpened():
        frame = cv2.rotate(bad_apple_cap.read()[1], cv2.ROTATE_180)

        for y in range(0, height):
            for x in range(0, width):
                blocks[Vec3(x,0,y)].color = color.rgb(frame[y, x][0], frame[y, x][1], frame[y, x][2])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)

        app.step()

if __name__ == "__main__":
    start()