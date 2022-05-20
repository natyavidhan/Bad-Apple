import cv2

vid = cv2.VideoCapture("src/Bad Apple.mp4")
success, image = vid.read()
count = 0
while success:
    cv2.imwrite("src/frames/frame%d.png" % count, image)
    success, image = vid.read()
    print('Read a new frame: ', success)
    count += 1