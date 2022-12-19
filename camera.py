import cv2
from pathlib import Path
from base_camera import BaseCamera
import time


class Camera(BaseCamera):
    video_source = 0
    paused = False
    paused_image = open(Path('assets/paused_image.png'), 'rb').read()

    def __init__(self):
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            if not Camera.paused:
                _, img = camera.read()

                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img)[1].tobytes()
            else:
                yield Camera.paused_image
            
    @staticmethod 
    def pause(pause):
        Camera.paused = pause
