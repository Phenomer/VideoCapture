#!/usr/bin/python3

import cv2
from datetime import datetime
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=1920)
parser.add_argument('--cam_height', type=int, default=1080)
parser.add_argument('--cam_fps', type=int, default=60)
parser.add_argument('--scale', type=float, default=1.0)
args = parser.parse_args()

def resize_frame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width, height))

def export_image(frame):
    t = datetime.now()
    export_dir = os.path.join("Capture", "{:0>2}{:0>2}{:0>2}".format(t.year, t.month, t.day))
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, "{:0>2}{:0>2}{:0>2}_{:0>2}{:0>2}{:0>2}_{:0>6}.png".format(
        t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond))
    cv2.imwrite(export_path, frame)
    print("Capture: {}".format(export_path))

def main():
    cap = cv2.VideoCapture(args.cam_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.cam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.cam_height)
    cap.set(cv2.CAP_PROP_FPS, args.cam_fps)
    print("width: {}, height: {}, fps: {}".format(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        cap.get(cv2.CAP_PROP_FPS)))

    fullscreen = False
    while True:
        flag, frame = cap.read()
        if flag:
            frame = resize_frame(frame, args.scale)
            if fullscreen:
                cv2.namedWindow('viewer', cv2.WINDOW_NORMAL)
                cv2.setWindowProperty('viewer', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('viewer', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        if key == ord("f"):
            fullscreen = not fullscreen
            cv2.destroyAllWindows()
        elif flag and key == ord(' '):
            export_image(frame)

if __name__ == "__main__":
    main()