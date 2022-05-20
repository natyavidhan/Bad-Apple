import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import json, os, time

RES = 9

frames = []

def load():
    start = time.time()
    for i in range(6572):
        x, y = [],[]
        img = Image.open(f"src/frames/frame{i}.png")
        img = img.resize((960//RES,720//RES))
        data = img.getdata()
        data = np.array(data)
        for index, value in enumerate(data):
            x_ = index % (960//RES)
            y_ = (720//RES) - index // (960//RES)
            if value[0] == 0:
                x.append(x_)
                y.append(y_)
        frames.append({'x':x,'y':y})
        print(i)
    print(f"Loaded {len(frames)} frames in {time.time()-start} seconds")
    start = time.time()
    json.dump(frames, open("src/frames.json", "w"))
    print(f"Dumped frames data in {time.time()-start} seconds")

print("Loading frames...")
if os.path.isfile("src/frames.json"):
    print("Frames data found, loading...")
    start = time.time()
    frames = json.load(open("src/frames.json"))
    print(f"Loaded {len(frames)} frames in {time.time()-start} seconds")
else:
    print("Frames data not found, loading from images...")
    load()


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
