# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class PolygonCalculation(object):
    def __init__(self, right_bound, left_bound):
        """Create a shapely-polygon"""
        p = np.vstack([right_bound, left_bound[::-1]])
        self.polygon = Polygon(p)

    def __call__(self, point_xy):
        """Check if point is inside polygon. Return boolean"""
        point = Point(point_xy[0], point_xy[1])
        return self.polygon.contains(point)
