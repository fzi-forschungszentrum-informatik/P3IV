# This file is part of the Interpolated Polyline (https://github.com/...),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)


import numpy as np  # original numpy
import warnings
from p3iv_utils_polyline.interpolated_polyline_segment import InterpolatedPolylineSegment


class InterpolatedPolyline(object):
    def __init__(self, xs, ys):
        self.N = len(xs)
        self._MAX_VALUE = np.finfo(np.float64).max

        if self.N < 3:
            warnings.warn("Number of support points is too low!")
        assert self.N == len(ys)
        assert self.N > 1

        self.xs = np.asarray(xs)
        self.ys = np.asarray(ys)

        self.segments = [None] * (self.N - 1)
        self.arclengths = np.empty(self.N)
        self.thetas = np.empty(self.N)

        self._fill_angles()
        self._fill_segments()
        self._fill_arclengths()

    def signed_distance(self, x, y):
        _, d, _ = self._get_closest_line_segment(x, y)
        return d

    def tangent(self, x, y):
        ind, d, lmda = self._get_closest_line_segment(x, y)
        tangent = self.segments[ind].tangent(x, y, d, lmda)
        return d, tangent

    def match(self, x, y):
        ind, d, lmda = self._get_closest_line_segment(x, y)

        # arclengths[ind] is the arc-length up until that segment
        arcl = self.arclengths[ind] + self.segments[ind].length(lmda)

        return arcl, d

    def oriented_match(self, x, y):
        ind, d, lmda = self._get_closest_line_segment(x, y)

        # arclengths[ind] is the arc-length up until that segment
        arcl = self.arclengths[ind] + self.segments[ind].length(lmda)

        tangent = self.segments[ind].tangent(x, y, d, lmda)

        return arcl, d, tangent

    def reconstruct(self, l, d):

        # Get base line segment and interpolate the rest
        if l < self.arclengths[1]:
            # first arclength is 0.
            i_base = 0
        else:
            for i_base in range(1, len(self.arclengths)):
                if l <= self.arclengths[i_base]:
                    break
            i_base = i_base - 1

        arcl_base = self.arclengths[i_base]
        arcl_remain = l - arcl_base

        assert arcl_base >= 0.0

        xB, yB, theta = self.segments[i_base].getBase()

        x_line = xB + arcl_remain * np.cos(theta)
        y_line = yB + arcl_remain * np.sin(theta)

        x = x_line + d * (-np.sin(theta))
        y = y_line + d * (np.cos(theta))

        return x, y

    def max_arclength(self):
        return self.arclengths[-1]

    # @numbajit(nopython=True)
    def numba_signed_distance(self, x, y):
        return self.signed_distance(x, y)

    def _fill_angles(self):
        # tangent vector angles
        for i in range(1, self.N - 1):
            dx = self.xs[i + 1] - self.xs[i - 1]
            dy = self.ys[i + 1] - self.ys[i - 1]
            self.thetas[i] = np.arctan2(dy, dx)

        # fill the initial one not with central differences
        # (cf. "Lanelets: Efficient Map Representation for Autonomous Driving", p. 4, left col.)
        self.thetas[0] = np.arctan2(self.ys[1] - self.ys[0], self.xs[1] - self.xs[0])

        self.thetas[-1] = np.arctan2(self.ys[-1] - self.ys[-2], self.xs[-1] - self.xs[-2])

    def _fill_segments(self):

        for i in range(self.N - 1):
            mode = "MIDDLE"
            if i == 0:
                mode = "FIRST"
            elif i == self.N - 2:
                mode = "LAST"

            self.segments[i] = InterpolatedPolylineSegment(
                self.xs[i], self.ys[i], self.thetas[i], self.xs[i + 1], self.ys[i + 1], self.thetas[i + 1], mode
            )

    def _fill_arclengths(self):
        self.arclengths[0] = 0
        # do not use np.cumsum for numba compability
        for i in range(1, self.N):
            self.arclengths[i] = self.arclengths[i - 1] + self.segments[i - 1].length()

    def _get_closest_line_segment(self, x, y):
        ind = 0
        d = self._MAX_VALUE
        lmda = 0
        for i in range(self.N - 1):
            tmp_d, tmp_lmda = self.segments[i](x, y)

            # check if it is the closest one
            if abs(tmp_d) < abs(d):
                ind = i
                d = tmp_d
                lmda = tmp_lmda
        return ind, d, lmda
