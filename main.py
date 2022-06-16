import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

import json, os, time

RES = 9


def load():
    frames = ""
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
    return frames

def decompress_frames(frames):
    frames = frames.split("\n")
    decompressed_frames = []
    for index, frame in enumerate(frames):
        # print(f"Frame: {frame}")
        if frame == "":
            continue
        lines = frame.split("|")
        frame_ = ""
        for line in lines:
            line_data_ = ""
            line_data = line.split(",")
            # print(f"Frame Line: {line}")
            for index, line_ in enumerate(line_data):
                # print(f"Line but in list format: {line_}")
                color, number = line_.split(" ")
                for i in range(int(number)):
                    frame_ += color
            frame_ += "\n"
        decompressed_frames.append(frame_)
    return decompressed_frames

def frames_to_coords(frames):
    data = []
    for frame in frames:
        frmae_data = {"white": {"x": [], "y": []}, "black": {"x": [], "y": []}}
        lines = frame.split("\n")
        for y_, line in enumerate(lines):
            for x_, px in enumerate(line):
                if px == "0":
                    frmae_data["white"]["x"].append(x_)
                    frmae_data["white"]["y"].append(y_)
                else:
                    frmae_data["black"]["x"].append(x_)
                    frmae_data["black"]["y"].append(y_)
        data.append(frmae_data)
    return data


def start_animation(frames):
    plt.ion()
    fig, ax = plt.subplots()
    x, y = [],[]
    bsc = ax.scatter(x,y, s=15, c='black')
    wsc = ax.scatter(x,y, s=15, c='white')
    plt.xlim(0,960//RES)
    plt.ylim(0,720//RES)
    plt.draw()

    for index, frame in enumerate(frames):
        # x, y = frame['x'], frame['y']
        # sc.set_offsets(np.c_[x,y])
        # fig.canvas.draw_idle()
        # plt.pause(0.006)
        wx, wy = frame['white']['x'], frame['white']['y']
        bx, by = frame['black']['x'], frame['black']['y']
        wsc.set_offsets(np.c_[wx,wy])
        bsc.set_offsets(np.c_[bx,by])
        fig.canvas.draw_idle()
        plt.pause(0.006)

    plt.waitforbuttonpress()

def main():
    print("Loading frames...")
    if os.path.isfile("src/frames.txt"):
        print("Frames data found, loading...")
        start = time.time()
        frames = open("src/frames.txt")
        frames = frames.readlines()
        print(f"Loaded {len(frames)} frames in {time.time()-start} seconds")
        frames = "".join(frames)
    else:
        print("Frames data not found, loading from images...")
        frames = load()

    print("Decompressing frames...")
    start = time.time()
    df = decompress_frames(frames)
    print(f"Decompressed {len(df)} frames in {time.time()-start} seconds")

    print("Converting frames to coords...")
    start = time.time()
    frames = frames_to_coords(df)
    print(f"Converted {len(frames)} frames in {time.time()-start} seconds")

    print("Starting animation...")
    start_animation(frames)

if __name__ == "__main__":
    main()