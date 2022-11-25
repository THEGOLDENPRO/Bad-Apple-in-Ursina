import sys
import threading
from typing import Dict
from ursina import Ursina, Entity, Vec3, Vec2, camera, Keys, held_keys, color, time, window, mouse, clamp, destroy, Audio, Color, Shader
from ursina.prefabs.first_person_controller import FirstPersonController
import fpstimer
import av
from PIL import ImageOps

window.borderless = True
window.size = (1200, 720)

blocks:Dict[Vec3, Entity] = {}

class UwUCamera(Entity):
    def __init__(self):
        super().__init__()

        self.controller = FirstPersonController()
        self.controller.gravity = 0
        self.controller.speed = 10
        self.controller.cursor.disable()

        self.controller.position = Vec3(30, 20, -57)

    def update(self):
        if held_keys["space"]:
            self.controller.position += (self.controller.up * 10) * time.dt

        if held_keys[Keys.left_shift]:
            self.controller.position += (self.controller.down * 10) * time.dt

        if held_keys[Keys.escape]:
            sys.exit(0)


class Block(Entity):
    def __init__(self, location:Vec3):
        super().__init__()

        blocks[location] = self

        self.model = "cube"
        self.position = location

def get_frames(video_path:str):
    cap = av.open(video_path)
    frames = cap.decode(video=0)
    return [ImageOps.flip(frame.to_image()) for frame in frames]

def start():
    app = Ursina()
    UwUCamera()
    
    # Get frames.
    bad_apple_frames = get_frames("./assets/bad_apple.mp4")

    # Grab the image dimensions.
    # ----------------------------
    height = bad_apple_frames[0].height; width = bad_apple_frames[0].width

    # Set up colours.
    # --------------
    BLACK = color.black; WHITE = color.white

    # Place blocks.
    # --------------
    for y in range(0, height):
        for x in range(0, width):
            Block(location=Vec3(x,y,0))
    
    # FPS Timer
    # ----------
    fps_timer = fpstimer.FPSTimer(12)

    # Play audio.
    # -------------
    bad_apple_audio = Audio("./bad_apple_audio.mp3")
    def start_audio(): time.sleep(0.5); bad_apple_audio.play()
    threading.Thread(target=start_audio).start()
    
    # Loop through each frame.
    # -------------------------
    for frame in bad_apple_frames:
        for y in range(0, height):
            for x in range(0, width):
                block:Entity = blocks[Vec3(x,y,0)]

                if frame.getpixel((x,y))[0] < 40:
                    if not block.color == BLACK: block.color = BLACK
                else:
                    if not block.color == WHITE: block.color = WHITE
                
                #blocks[Vec3(x,0,y)].color = color.rgb(frame[y, x][0], frame[y, x][1], frame[y, x][2])
        
        app.step()
        fps_timer.sleep()

if __name__ == "__main__":
    start()