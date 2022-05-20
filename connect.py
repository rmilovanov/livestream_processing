import json
import cv2
import pafy

import config


def create_specs():
    url = config.live_video_url
    video = pafy.new(url)
    specs = video.__dict__

    with open("specs.json", "w") as sf:
        json.dump(specs, sf, indent=4)


class Format:
    def __init__(self, data):
        self.url = data.get("url")
        self.manifest_url = data.get("manifest_url")
        self.fps = data.get("fps")
        self.width = data.get("width")
        self.height = data.get("height")


def get_stream_url_from_specs():
    with open("specs.json", "r") as f:
        specs = json.load(f)

    formats = [Format(el) for el in specs["_ydl_info"]["formats"]]

    stream_url = formats[0].manifest_url
    fps = 30

    formats.sort(key=lambda x: x.width, reverse=True)
    formats = [el for el in formats[1:] if el.width < 800]
    for fmt in formats:
        print("Trying format {}-{}x{}".format(fmt.fps, fmt.width, fmt.height))
        stream_url = fmt.url
        cap = cv2.VideoCapture(stream_url)
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)

        if not ret:
            continue
        else:
            return stream_url, fps
