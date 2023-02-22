import numpy as np
import cv2
from camera import Camera, FakeCamera
import pathlib

camera = Camera(0)
while True:
    # Capture frame-by-frame
    ret, frame = camera.get_frame()
    
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)

    if key & 0xFF == ord('w'):
        filename = pathlib.Path('images')
        filename.mkdir(parents=True, exist_ok=True)
        #find file name that doesn't exist
        i = 0
        while True:
            filename = pathlib.Path('images', f'img{i}.png')
            if not filename.exists():
                break
            i += 1
        camera.save_frame(str(filename.absolute()))

    if key & 0xFF == ord('q'):
        break