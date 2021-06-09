# This file is part of the Interpolated Polyline (https://github.com/...),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)


from __future__ import division
import numpy as np
import warnings


# @numbajit
def hypot(a, b):
    # do not use np.hypot(a, b); may not work well with autodiff & jit
    return (a ** 2 + b ** 2) ** 0.5


class InterpolatedPolylineSegment(object):
    def __init__(self, xB, yB, thetaB, xT, yT, thetaT, mode):
        self.xB = xB
        self.yB = yB
        self.thetaB = thetaB
        self.thetaT = thetaT

        self.theta = np.arctan2(yT - yB, xT - xB)
        self.cosTheta = np.cos(self.theta)
        self.sinTheta = np.sin(self.theta)
        self.hyp = hypot(yT - yB, xT - xB)

        self.mB = np.tan(thetaB - self.theta)
        self.mT = np.tan(thetaT - self.theta)
        self.mode = mode
        self._MAX_VALUE = 1e10
        # do not use float(inf)

    def __call__(self, x, y):

        xH, yH = self._convertHesseNormal(x, y)

        # signum on line-aligned coordinate system is the sign of y-axis
        signum = np.sign(yH)

        # calculate interpolation factor
        lmda = self._getLambda(self.hyp, self.mB, self.mT, xH, yH)

        valid, lmda = self._clipLambda(lmda)

        if valid:
            # this is the segment, that may be closest to the point (for mode='MIDDLE')
            d = signum * self._normalDistance(self.hyp, xH, yH, lmda)
            # print("MIDDLE ", "x: ", xr, "y: ", yr,"d : ", d, "lambda : ", lmda)
        else:
            d = signum * self._MAX_VALUE

        return d, lmda

    def length(self, lmda=1.0):
        return lmda * self.hyp

    def tangent(self, x, y, d, lmda):
        xH, yH = self._convertHesseNormal(x, y)
        # add 'theta' to get tangent in global Cartesian frame
        tangent = self._getTangent(self.hyp, xH, yH, d, lmda, self.mB, self.mT) + self.theta
        return tangent

    def getBase(self):
        return self.xB, self.yB, self.theta

    def _clipLambda(self, lmda):
        """
        Check interpolation factor if it is valid and clip it
        """
        valid = True

        if (lmda < 0.0) or (lmda > 1.0):
            if self.mode == "MIDDLE":
                # skip to the next segment in polyline
                valid = False

            elif self.mode == "FIRST":
                if lmda < 0.0:
                    lmda = 0.0
                elif lmda > 1.0:
                    valid = False

            elif self.mode == "LAST":
                # let the last segment's lambda be flexible
                if abs(lmda) > 1.0:
                    lmda = 1.0
                elif lmda < -1.0:
                    valid = False

            else:
                warnings.warn("An unexpected case detected!")
                valid = False

        return (valid, lmda)

    def _convertHesseNormal(self, x, y):
        """
        Convert to Hesse-normal form; aka line-aligned coordinate frame
        """

        # calculate the difference of the given point to the one end of the line
        xx = x - self.xB
        yy = y - self.yB

        # rotate point Theta clockwise for line-referenced coordinates
        xH = xx * self.cosTheta + yy * self.sinTheta
        yH = -xx * self.sinTheta + yy * self.cosTheta

        return xH, yH

    @staticmethod
    def _getTangent(l, xH, yH, d, lmda, mB, mT):
        """
        Get tangent vector angle in line-aligned coordinates
        """
        if d == 0:
            return lmda * mB + (1 - lmda) * mT
        dx = np.divide(-1 * (lmda * l - xH), d)
        dy = np.divide(-1 * (-yH), d)
        dTheta = np.arctan2(dy, dx)  # normal vector
        tangent = dTheta - np.pi / 2  # tangent vector
        return tangent

    @staticmethod
    def _getLambda(l, mb, mt, xH, yH):
        """
        Calculate interpolation factor lambda
        """
        # cf. Eq. (3.9) in Diss. Ziegler
        return (xH + yH * mb) / (l - yH * (mt - mb))

    @staticmethod
    def _normalDistance(l, xH, yH, lmda):
        """
        Find the normal distance in Hesse normal form
        """
        return hypot((lmda * l - xH), yH)
