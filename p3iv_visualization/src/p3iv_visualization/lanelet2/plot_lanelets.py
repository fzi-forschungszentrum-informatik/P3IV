# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from matplotlib.axes import Axes
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


class PlotLanelets(object):
    def __init__(self, axes):
        assert isinstance(axes, Axes)
        self.ax = axes

    def __call__(self, llts, facecolors="None", edgecolors="red", alpha=1.0):

        if isinstance(llts, list):
            lanelet_polygon = self._laneletSequencePolygon(llts)
        else:
            lanelet_polygon = [self._laneletPolygon(llts)]
        patches = PatchCollection(lanelet_polygon, facecolors=facecolors, edgecolors=edgecolors, alpha=alpha)
        self.ax.add_collection(patches)

    def clear(self):
        for c in self.ax.collections:
            c.remove()

    @staticmethod
    def _laneletPolygon(llt):
        points = [[pt.x, pt.y] for pt in llt.polygon2d()]
        return Polygon(points, True)

    @classmethod
    def _laneletSequencePolygon(cls, llt_list):
        polygons4lanelets = []
        for ll in llt_list:
            polygons4lanelets.append(cls._laneletPolygon(ll))
        return polygons4lanelets
