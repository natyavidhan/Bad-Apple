import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

import json, os, time

RES = 9

frames = ""


def load():
    global frames
    start = time.time()
    
    vid = cv2.VideoCapture("src/Bad Apple.mp4")
    success, image = vid.read()
    count = 0
    while success:
        frame_data = ""
        line_data = []
        image = Image.fromarray(np.uint8(image))
        
        image = image.resize((960//RES,720//RES))
        data = image.getdata()
        data = np.array(data)
        curr_line_data = ""
        curr_line = 0
        for index, value in enumerate(data):
            line = index // (960//RES)
            if line != curr_line:
                line_data.append(curr_line_data)
                curr_line_data = ""
                curr_line = line
            if value[0] == 0:
                curr_line_data += "1"
            else:
                curr_line_data += "0"
        line_data.append(curr_line_data)

        for line in line_data:
            sudo_line_data = ""
            curr_color = 1
            curr_color_count = 0
            for px in line:
                if curr_color == int(px):
                    curr_color_count += 1
                else:
                    sudo_line_data += f"{curr_color} {curr_color_count},"
                    curr_color = int(px)
                    curr_color_count = 1
            sudo_line_data += f"{curr_color} {curr_color_count}"
            frame_data += sudo_line_data + "|"

        frame_data = frame_data[:-1]
        
        frames += f"{frame_data}\n"
        print(f"Frame {count+1} Extracted")

        success, image = vid.read()
        count += 1
        
    print(f"Loaded {count+1} frames in {time.time()-start} seconds")
    start = time.time()
    with open("src/frames.txt", "w") as f:
        f.write(frames)
    print(f"Dumped frames data in {time.time()-start} seconds")


def start_animation():
    plt.ion()
    fig, ax = plt.subplots()
    x, y = [],[]
    sc = ax.scatter(x,y, s=15, c='black')
    plt.xlim(0,960//RES)
    plt.ylim(0,720//RES)
    plt.draw()

    for index, frame in enumerate(frames):
        x, y = frame['x'], frame['y']
        sc.set_offsets(np.c_[x,y])
        fig.canvas.draw_idle()
        plt.pause(0.006)

    plt.waitforbuttonpress()

def main():
    print("Loading frames...")
    if os.path.isfile("src/frames.json"):
        print("Frames data found, loading...")
        start = time.time()
        frames = json.load(open("src/frames.json"))
        print(f"Loaded {len(frames)} frames in {time.time()-start} seconds")
    else:
        print("Frames data not found, loading from images...")
        load()

if __name__ == "__main__":
    load()