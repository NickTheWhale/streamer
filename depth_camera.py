import cv2
from pathlib import Path
from base_camera import BaseCamera
import pyrealsense2 as rs
import numpy as np


class Camera(BaseCamera):
    video_source = 'COLOR'
    paused = False
    paused_image = open(Path('assets/paused_image.png'), 'rb').read()
    colorizer = rs.colorizer()

    def __init__(self):
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        """set DEPTH or COLOR"""
        Camera.video_source = source

    @staticmethod
    def frames():
        pipeline = Camera._connect_camera()

        while True:
            # read current frame
            if not Camera.paused:
                frames = pipeline.wait_for_frames()
                if Camera.video_source == 'DEPTH':
                    depth_frame = frames.get_depth_frame()
                    
                    if not depth_frame:
                        continue
                    
                    color_depth_frame = Camera.colorizer.colorize(depth_frame)
                    color_depth_image = np.asanyarray(color_depth_frame.get_data())
                    # encode as a jpeg image and return it
                    yield cv2.imencode('.jpg', color_depth_image)[1].tobytes()
                    
                elif Camera.video_source == 'COLOR':
                    color_frame = frames.get_color_frame()
                    
                    if not color_frame:
                        continue
                    
                    color_image = np.asanyarray(color_frame.get_data())
                    # encode as a jpeg image and return it
                    yield cv2.imencode('.jpg', color_image)[1].tobytes()
                    
            else:
                yield Camera.paused_image
            
    @staticmethod 
    def pause(pause):
        Camera.paused = pause
        
    def _connect_camera():
        # Configure depth and color streams
        print('Starting camera pipeline.')
        pipeline = rs.pipeline()
        config = rs.config()
        # Get device product line for setting a supporting resolution
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        pipeline.start(config)
        
        return pipeline
