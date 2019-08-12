from shapely.geometry import Point, LineString
import cv2
import numpy as np


class Threshold:

    def __init__(self, name, points, color):
        self.name = name
        self.line = LineString(points)
        self.parallel_in = self.line.parallel_offset(30, side='left')
        self.parallel_out = self.line.parallel_offset(30, side='right')

        length = self.line.length
        self.midpoint = self.line.interpolate(length/2)
        self.mid_in = self.parallel_in.interpolate(length/2)
        self.mid_out = self.parallel_out.interpolate(length/2)

        self.p_in = int(self.mid_in.x), int(self.mid_in.y)
        self.p_out = int(self.mid_out.x), int(self.mid_out.y)

        t_array = np.array(self.line)
        self.t_vec = t_array[1] - t_array[0]

        self.color = color
        self.counter = {"in": 0, "out": 0}

    def check(self, line):
        if self.line.intersects(line):
            p_array = np.array(line)
            p_vec = p_array[1] - p_array[0]
            direction = np.inner(self.t_vec, p_vec)
            if direction > 0:
                self.counter["in"] += 1
                return True
            elif direction < 0:
                self.counter["out"] += 1
                return True

    def draw(self, image):
        print(self.counter)
        line = np.array(self.line, np.uint32)
        cv2.line(
                image,
                tuple(line[0]),
                tuple(line[1]),
                self.color,
                2
                )

        cv2.circle(
            image,
            tuple(self.p_in),
            18,
            self.color,
            -9
            )

        in_count = self.counter["in"]
        cv2.putText(
            image,
            "{}:{}".format(self.name, str(in_count)),
            (int(self.p_in[0])-17, int(self.p_in[1])+5),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (0,0,0),
            1
            )

        out_count = self.counter["out"]
        cv2.circle(
            image,
            tuple(self.p_out),
            18,
            self.color,
            -9
            )

        cv2.putText(
            image,
            "{}:{}".format(self.name, str(out_count)),
            (int(self.p_out[0])-17, int(self.p_out[1])+5),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (0,0,0),
            1
            )
