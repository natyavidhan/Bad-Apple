import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

import json, os, time

RES = 9

def progress_bar(progress, total):
    percent = 100 * (progress / total)
    bar = '█' * int(percent) + "▒" * (100 - int(percent))
    print(f"\r[{bar}] {percent:.2f}%", end="\r")


def load():
    frames = ""
    start = time.time()
    
    vid = cv2.VideoCapture("src/Bad Apple.mp4")
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    success, image = vid.read()
    count = 0
    progress_bar(count, total_frames)
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

        success, image = vid.read()
        count += 1
        progress_bar(count, total_frames)
        
    print(f"\nLoaded {count+1} frames in {time.time()-start} seconds")
    start = time.time()
    with open("src/frames.txt", "w") as f:
        f.write(frames)
    print(f"Dumped frames data in {time.time()-start} seconds")
    return frames

def decompress_frames(frames):
    if os.path.isfile("cache/decompressed_frames.json"):
        df = json.load(open("cache/decompressed_frames.json"))
        return df
    frames = frames.split("\n")
    decompressed_frames = []
    progress_bar(0, len(frames))
    for findex, frame in enumerate(frames):
        if frame == "":
            continue
        lines = frame.split("|")
        frame_ = ""
        for line in lines:
            line_data_ = ""
            line_data = line.split(",")
            for index, line_ in enumerate(line_data):
                color, number = line_.split(" ")
                for i in range(int(number)):
                    frame_ += color
            frame_ += "\n"
        decompressed_frames.append(frame_)
        progress_bar(findex+1, len(frames)-1)
    print("\n")
    if not os.path.isdir("cache"):
        os.mkdir("cache")
    with open("cache/decompressed_frames.json", "w") as f:
        json.dump(decompressed_frames, f)
    return decompressed_frames

def frames_to_coords(frames):
    data = []
    progress_bar(0, len(frames))
    for index, frame in enumerate(frames):
        frmae_data = {"white": {"x": [], "y": []}, "black": {"x": [], "y": []}}
        lines = frame.split("\n")
        for y_, line in enumerate(lines):
            for x_, px in enumerate(line):
                x = x_
                y = 720//RES - y_
                if px == "0":
                    frmae_data["white"]["x"].append(x)
                    frmae_data["white"]["y"].append(y)
                else:
                    frmae_data["black"]["x"].append(x)
                    frmae_data["black"]["y"].append(y)
        data.append(frmae_data)
        progress_bar(index+1, len(frames))
    print("\n")
    return data


def start_animation(frames):
    plt.ion()
    fig, ax = plt.subplots()
    x, y = [],[]
    wsc = ax.scatter(x,y, s=15, c='white')
    bsc = ax.scatter(x,y, s=15, c='black')
    plt.xlim(0,960//RES)
    plt.ylim(0,720//RES)
    plt.draw()

    for index, frame in enumerate(frames):
        wx, wy = frame['white']['x'], frame['white']['y']
        bx, by = frame['black']['x'], frame['black']['y']
        wsc.set_offsets(np.c_[wx,wy])
        bsc.set_offsets(np.c_[bx,by])
        fig.canvas.draw_idle()
        plt.pause(0.0000001)

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