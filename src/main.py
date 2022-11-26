from datetime import timedelta
import sys
import threading
from typing import Dict
from ursina import Ursina, Entity, Vec3, Vec2, Keys, held_keys, color, time, window, Audio
from ursina.prefabs.first_person_controller import FirstPersonController
import fpstimer
import av
from PIL import ImageOps

window.borderless = False
window.size = (1200, 720)

blocks:Dict[Vec3, Entity] = {}

class UwUCamera(Entity):
    def __init__(self):
        super().__init__()

        self.controller = FirstPersonController()
        self.controller.gravity = 0
        self.controller.speed = 10
        self.controller.cursor.disable()

        self.controller.position = Vec3(30, 20, -67)

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
    print("Decoding all frames...")
    cap = av.open(video_path)
    frames = cap.decode(video=0)
    return [ImageOps.flip(frame.to_image()).resize((70, 50)) for frame in frames], timedelta(microseconds=cap.duration).total_seconds()

def place_blocks(width:int, height:int):
    print("Placing blocks...")

    # Place blocks.
    # --------------
    for y in range(0, height):
        for x in range(0, width):
            block = Block(location=Vec3(x,y,0))
            sys.stdout.write(f"Placed block at {block.position}\n")

    print("Done placing blocks!")


def start():
    # Get video frames.
    bad_apple_frames, duration_in_seconds = get_frames("./assets/bad_apple.mp4")

    # Reducing frame rate.
    del bad_apple_frames[1::2]; del bad_apple_frames[1::5]
    target_frame_rate = (len(bad_apple_frames)/duration_in_seconds)

    # Grab the image dimensions.
    # ----------------------------
    height = bad_apple_frames[0].height; width = bad_apple_frames[0].width

    # Set up colours.
    # --------------
    BLACK = color.black; WHITE = color.white

    # Initialize engine and audio.
    # --------------------------------
    app = Ursina()
    bad_apple_audio = Audio("./assets/bad_apple.mp4", autoplay=False)
    UwUCamera()

    # Place all blocks.
    # --------------------
    place_blocks(width, height)
    
    # FPS Timer
    # ----------
    fps_timer = fpstimer.FPSTimer(target_frame_rate)
    print(f"Target frame rate -> {target_frame_rate}")

    # Play audio.
    # -------------
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