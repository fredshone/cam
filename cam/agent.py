from collections import OrderedDict
import numpy as np
import os
from shapely.geometry import Point, LineString
import PIL.Image as Image
from PIL import ImageFont
from PIL import ImageDraw
from matplotlib import pyplot as plt
import cv2


class MyOrderedDict(OrderedDict):
    def last(self):
        k = list(self.keys())[-1]
        return k, self[k]
    def last2(self):
        k = list(self.keys())[-2]
        return k, self[k]


class Agent:

    def __init__(self, ident, color, thresholds):
        self.bb = None
        self.loc = None
        self.time = None
        self.trajectory = MyOrderedDict()
        self.speed = None
        self.direction = None
        self.total_dist = 0
        self.active = False
        self.ident = ident
        self.color = color
        self.threshold_lag = 100  # frames
        self.thresholds = thresholds
        self.threshold_history = {}
        self.flag = False

    def add_detection(self, bb, time):
        ####### left top width height
        l,t,w,h = bb
        self.bb = bb
        self.loc = Point((int(l + w/2), int(t + h)))
        self.time = time
        self.trajectory[time] = self.loc

        if self.active:
            self.build_trace(time)
            self.check_thresholds(time)

        self.active = True

    def build_trace(self, time):
        t_, loc_ = self.trajectory.last2()
        t_diff = time - t_

        dist = self.loc.distance(loc_)

        self.speed = dist / t_diff
        self.direction = (self.loc.x - loc_.x), (self.loc.y - loc_.y)
        self.total_dist += dist

    def check_thresholds(self, time):
        line = LineString((self.trajectory.last()[1],
            self.trajectory.last2()[1]))
        for threshold in self.thresholds:
            last_trigger = self.threshold_history.get(threshold.name)
            if last_trigger and (time - last_trigger) < self.threshold_lag:
                continue
            if threshold.check(line):
                self.threshold_history[threshold.name] = time
                self.flag = threshold.color

    def draw(self, image):
        if self.flag:
            color = self.flag
        else:
            color = self.color
        self.add_bb(image, color)
        self.add_point(image, color)
        self.add_traj(image, color)
        self.flag = None 

    def add_bb(self, image, color):
        ####### left top width height
        left, top, width, height = self.bb
        right = left + width
        bottom = top + height

        cv2.rectangle(
                image,
                (left, top),
                (right, bottom),
                color,
                1,
                )

    def add_point(self, image, color):
        ####### left top width height
        centre = int(self.loc.x)
        bottom = int(self.loc.y)

        cv2.circle(
                image,
                (centre, bottom),
                4,
                color,
                -2
        )

    def add_traj(self, image, color):
        traj = np.array([(p.x, p.y) for p in self.trajectory.values()], np.int32)

        cv2.polylines(
                image,
                [traj],
                False,
                color,
                1
                )

def convert_to_rgb(cmap):
    r, g, b = [int(c * 255) for c in cmap[:3]]
    return r, g, b


def get_colour(size=20):
    cmap = plt.cm.get_cmap('tab20', size)
    index = np.random.choice(list(range(size)), size=size, replace=False, p=None)
    while True:
        for i in index:
            yield convert_to_rgb(cmap(i))

