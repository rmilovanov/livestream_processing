from datetime import datetime
from time import time, sleep

import pickle
import cv2


class FrameData:
    def __init__(self, frame, ts, fps, size, count):
        self.frame = frame
        self.ts = ts
        self.fps = fps
        self.width = size[0]
        self.height = size[1]
        self.count = count


class LocalBuffer:
    file = "local_buffer"

    @classmethod
    def save(cls, frames, fps):
        '''print("{} saving local buffer {} frames {} fps ".format(
            datetime.now().strftime('%H:%M:%S'), len(frames), fps))'''
        data = {"frames": frames, "fps": fps}
        with open(cls.file, 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def read(cls):
        with open(cls.file, 'rb') as f:
            try:
                data = pickle.load(f)
            except Exception:
                return None, 0
            frames, fps = data["frames"], int(data["fps"])
            print("{} local buffer read {} frames {} fps".format(
                datetime.now().strftime('%H:%M:%S'), len(frames), fps))
            return frames, fps


class BufferGenerator:
    def __init__(self, buffer_cap, fps):
        self.buffer_cap = buffer_cap
        self.frames = []
        self.fps = fps
        self.counter = 0

    def put(self, frame_data: FrameData):
        self.counter += 1
        self.frames.append(frame_data)
        if self.counter > self.buffer_cap:
            first_frame = self.frames[0].count
            last_frame = self.frames[-1].count
            print("{} Save {} frames from {} to {} with {} fps to local buffer".format(
                datetime.now().strftime('%H:%M:%S'), self.counter, first_frame, last_frame, self.fps))
            frames = [dat.frame for dat in self.frames]
            LocalBuffer.save(frames, self.fps)
            self.frames = []
            self.counter = 0


class StreamGenerator:
    @staticmethod
    def gen_frames():
        """Concat frame one by one and show result"""
        while True:
            frames, fps = LocalBuffer.read()
            if frames:
                print("read {} frames ".format(len(frames)))
                for frame in frames:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    sleep(1 / fps)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


class SimpleProcessor:
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.cap = cv2.VideoCapture(self.stream_url)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_counter = 0

    def frames(self):
        while True:
            ret, frame = self.cap.read()  # bool, nympy.ndarray
            self.frame_counter += 1
            if ret:
                size = frame.shape
                print("{} size {}  time: {}".format(self.frame_counter, size, datetime.now().strftime('%H:%M:%S')), end="\r")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                yield FrameData(gray, time(), self.fps, size, self.frame_counter)
