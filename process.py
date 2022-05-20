import cv2
import zmq
from time import time
import json
from datetime import datetime

from models import FrameData




cap = cv2.VideoCapture(stream_url)
print(cap)


while True:
    ret, frame = cap.read()   # bool, nympy.ndarray
    counter += 1
    if ret:
        size = frame.shape
        print("{} size {}  time: {}".format(counter, size, datetime.now().strftime('%H:%M:%S')), end="\r")
        if counter > 120:
            dur = time() - start
            fps = cap.get(cv2.CAP_PROP_FPS)
            print("dur {} frames: {}  --> {} per second".format(dur, counter, fps))
            counter = 0
            start = time()
        #dst.send_pyobj(dict(frame=frame, ts=time()))
        data = FrameData(frame, time(), fps)
        dst.send_pyobj(data)