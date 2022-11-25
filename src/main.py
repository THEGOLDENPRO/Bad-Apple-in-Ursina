import sys
import threading
import cv2
from typing import Dict
from ursina import Ursina, Entity, Vec3, Vec2, camera, Keys, held_keys, color, time, window, mouse, clamp, destroy
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

        self.controller.position = Vec3(0, 42, 0)

    def update(self):
        if held_keys["space"]:
            self.controller.position += (self.controller.up * 8) * time.dt

        if held_keys[Keys.left_shift]:
            self.controller.position += (self.controller.down * 8) * time.dt

        if held_keys[Keys.escape]:
            sys.exit(0)


class BadApple(Entity):
    def __init__(self):
        super().__init__()

        self.bad_apple_cap = cv2.VideoCapture("./output.mp4")

        # Get first frame.
        frame = self.bad_apple_cap.read()[1]

        # Grab the image dimensions
        self.height = frame.shape[0]
        self.width = frame.shape[1]
    
    def start_render(self):
        while self.bad_apple_cap.isOpened():
            frame = self.bad_apple_cap.read()[1]

            # loop over the image, pixel by pixel
            for y in range(0, self.height):
                for x in range(0, self.width):
                    # threshold the pixel
                    #sys.stdout.writelines(f"{frame[y, x]}\n")

                    if Vec3(x,0,y) in blocks: destroy(blocks[Vec3(x,0,y)])
                    Block(location=(x,0,y)).color = color.rgb(frame[y, x][0], frame[y, x][1], frame[y, x][2])
                time.sleep(0.2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass

    def input(self, key):
        if key == "m":
            render_thread = threading.Thread(target=self.start_render)
            render_thread.setDaemon(True)
            render_thread.start()


class Block(Entity):
    def __init__(self, location:Vec3):
        super().__init__()

        blocks[location] = self

        self.model = "cube"
        self.position = location
        self.collider = "box"

def start_engine():
    app = Ursina()

    UwUCamera()
    BadApple()

    Block(location=Vec3(0,0,0))
    
    app.run()

if __name__ == "__main__":
    start_engine()