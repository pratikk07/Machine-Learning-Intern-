# util.py

import numpy as np

def get_angle(a, b, c):
    """Calculate the angle between three points (a, b, c) with b as the vertex."""
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    """Calculate the distance between two points given a list of coordinates."""
    if len(landmark_list) < 2:
        return None
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])
