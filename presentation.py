import numpy as np, sys, cv2

def onChange_gaussian(value):
    global powerGaussian
    powerGaussian = value

cap1 = cv2.VideoCapture('foreground.mp4')

if not cap1.isOpened():
    print('video open failed!')
    sys.exit()

cap2 = cv2.VideoCapture('background.mp4')

if not cap2.isOpened():
    print('video open failed!')
    sys.exit()

writer = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'X264'), 29.0, (270, 480), False)
if writer.isOpened() == False: raise Exception("동영상 파일 개방 안됨")

w1 = 270
h1 = 480

fps = cap1.get(cv2.CAP_PROP_FPS)
delay = int(1000/fps)
frame_cnt = 0
addGaussian = 1
powerGaussian = 1
compositFlag = False
gaussian = False
tb1 = False

while True:
    ret1, frame1 = cap1.read()
    if not ret1: break
    frame_cnt += 1
    frame1 = cv2.resize(frame1, (w1, h1))

    if compositFlag:
        ret2, frame2 = cap2.read()
        if not ret2: break
        frame2 = cv2.resize(frame2, (w1, h1))
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (40, 50, 50), (80, 255, 255))
        if gaussian:
            frame2 = cv2.GaussianBlur(frame2, (0, 0), powerGaussian)
        cv2.copyTo(frame2, mask, frame1)

    if 0 <= frame_cnt < 200:
        cv2.rectangle(frame1, (35, 400, 200, 55), (223, 225, 245), cv2.FILLED)
        cv2.putText(frame1, "Me: I'm finally coming", (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        cv2.putText(frame1, "to go to school.", (85, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 0))

    elif 300 <= frame_cnt < 400:
        cv2.rectangle(frame1, (35, 400, 200, 55), (223, 225, 245), cv2.FILLED)
        cv2.putText(frame1, 'Me: I want to take', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        cv2.putText(frame1, "a picture.", (85, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 0))

    elif 500 <= frame_cnt <680:
        frame1 = cv2.GaussianBlur(frame1, (0, 0), addGaussian)
        if addGaussian < 5:
            addGaussian += 1
        cv2.rectangle(frame1, (35, 400, 200, 55), (223, 225, 245), cv2.FILLED)
        cv2.putText(frame1, 'Me: The focus is', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        cv2.putText(frame1, "so blurry. Hmm...", (85, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 0))

    elif 680 <= frame_cnt < 780:
        frame1 = cv2.GaussianBlur(frame1, (0, 0), addGaussian)
        if addGaussian > 1:
            addGaussian -= 1

    elif 680 <= frame_cnt < 780:
        cv2.rectangle(frame1, (35, 400, 200, 30), (223, 225, 245), cv2.FILLED)
        cv2.putText(frame1, 'Me: Oh, no!', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    elif 1050 <= frame_cnt < 1351:
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame1 = cv2. Canny(frame1, 50, 200)
        cv2.rectangle(frame1, (35, 400, 200, 55), (223, 225, 245), cv2.FILLED)
        cv2.putText(frame1, 'Me: What the..? My ', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        cv2.putText(frame1, "phone got weird...", (85, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 0))

    writer.write(frame1)
    cv2.imshow('frame', frame1)

    key = cv2.waitKey(delay)

    if not tb1:
        cv2.createTrackbar('gaussian', 'frame', 1, 5, onChange_gaussian)
        tb1 = True

    if key == ord(' '):
        compositFlag = not compositFlag
    elif key == ord('g'):
        gaussian = not gaussian

cap1.release()
cap2.release()
writer.release()

cv2.destroyAllWindows()
