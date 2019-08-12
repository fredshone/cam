import PIL.Image as Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import os
import cv2

from cam import agent
from cam import count

def load_detections(path):
    return np.loadtxt(path, delimiter=',')

def get_num(string):
    return int(''.join(s for s in string if s.isdigit()))

def generate_frames(path):
    image_names = [n for n in os.listdir(path) if n[-4:] == ".jpg"]
    image_names = sorted(image_names)
    for image_name in image_names:
        yield os.path.join(path, image_name), get_num(image_name)

def load_thresholds():
    # define as clockwide around INSIDE direction
    threshold_names = (
            'A',
            'B',
            'C'
            )
    threshold_coords = (
            ((270,360),(550,530)),
            ((770,400),(550,530)),
            ((700, 350), (900, 370))
                )
    colors = (
            (255,0,0),
            (0,255,0),
            (0,0,255)
            )
    thresholds = []
    for name, points, color in zip(threshold_names, threshold_coords, colors):
        thresholds.append(count.Threshold(name, points, color))
    return thresholds

agents = {}

detections_path = os.path.join('data', 'north_trim', 'sample1', 'tracking.txt')
images_path = os.path.join('data', 'north_trim', 'sample1', 'img1')

frames = generate_frames(images_path)
thresholds = load_thresholds()
colours = agent.get_colour()

# get detections

detections = load_detections(detections_path)

for image_path, frame in frames:

    frame_dets = detections[detections[:,0] == frame]

    image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)

    for det in frame_dets:
        det_frame = det[0]
        assert det_frame == frame
        ident = int(det[1])
        bb = [int(p) for p in det[2:6]]

        if not agents.get(ident):
            agents[ident] = agent.Agent(ident, next(colours), thresholds)

        agents[ident].add_detection(bb, frame)
        agents[ident].draw(image)

    for threshold in thresholds:
        threshold.draw(image)

    cv2.imshow('1', image)
    cv2.imwrite(os.path.join('frames', f'frame{frame}.png'), image)

    key = cv2.waitKey(100)

    if key & 255 == 27:  # ESC
        print("terminating")
        break

for threshold in thresholds:
    print(f"> threshold {threshold.name}: {threshold.counter}")
