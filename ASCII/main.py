import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

import json, os, time, sys

from functions import convert, toImage

RES = 9

def progress_bar(progress, total):
    percent = 100 * (progress / total)
    bar = '█' * int(percent) + "▒" * (100 - int(percent))
    print(f"\r[{bar}] {percent:.2f}%", end="\r")



def load():
    frames = ""
    start = time.time()
    s, e = sys.argv[1], sys.argv[2]
    vid = cv2.VideoCapture("../src/Bad Apple.mp4")
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    success, image = vid.read()
    count = 0
    while success:
        if count >= int(s) and count <= int(e):
            start_ = time.time()
            frame_data = ""
            line_data = []
            image = Image.fromarray(np.uint8(image))
            image = image.resize((960//RES,720//RES))

            img_str = convert(image, 1)
            toImage(img_str, str(count))
            print(f"Frame {count} took {time.time() - start_} seconds")
        success, image = vid.read()
        count += 1

    print(f"Total time: {time.time() - start} seconds")

load()