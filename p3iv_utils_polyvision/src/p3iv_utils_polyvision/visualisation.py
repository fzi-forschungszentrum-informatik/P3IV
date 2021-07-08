# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
import math

import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection

from p3iv_utils_polyvision_pyapi import VisibleArea

precision = 6


class Car(object):
    """
    A Car
    """

    def __init__(self, fieldOfViewContour, position, yawAngle):
        self._fieldOfView = fieldOfViewContour
        self._position = 0
        self._yawAngle = 0
        self.updateCarPose(position, yawAngle)

    @property
    def position(self):
        """The position of the Car as 1x2 NumpyArray"""
        return self._position

    # no setter: use updateCarPose
    # @position.setter
    # def position(self, newPos):
    #     if newPos.shape == (1, 2):
    #         self._position = newPos
    #         self._fov = affineTransformationOfPoylgonList(
    #             self._fieldOfView, self._yawAngle, self._position, precision-3)

    @property
    def yawAngle(self):
        """The yaw angle of the car"""
        return self._yawAngle

    # no setter: use updateCarPose
    # @yawAngle.setter
    # def yawAngle(self, newYawAngle):
    #     self._yawAngle = newYawAngle
    #     self._fov = affineTransformationOfPoylgonList(
    #         self._fieldOfView, self._yawAngle, self._position, precision-3)

    @property
    def fieldOfView(self):
        """The field of view contour"""
        return self._fieldOfView

    # @fieldOfView.setter
    # def fieldOfView(self, newFieldOfViewContour):
    #     self._fieldOfView = newFieldOfViewContour

    def updateCarPose(self, deltaPosition, deltaYawAngle):
        self._position += deltaPosition
        self._yawAngle += deltaYawAngle
        # affine transformation of field of view
        self._fieldOfView = affineTransformationOfPoylgonList(
            self._fieldOfView, deltaYawAngle, deltaPosition, precision - 1
        )

    def getVisibleArea(self, perceptedPolygons):
        # create visibleArea object for calculations
        visA = VisibleArea(self._position[0], self._position[1], self._fieldOfView, precision)
        # add transformed percepted polygons
        visA.addPolygons(perceptedPolygons)
        # calculate visible area
        visAreaPoly = visA.calculateVisibleArea2()
        # clear polygons
        visA.clearPolygons()
        # del visibleArea object
        del visA
        return visAreaPoly


def affineTransformationOfPoylgonList(polylist, angle, offset, precision):
    for i in range(0, len(polylist)):
        polylist[i] = affineTransformationOfPolygon(polylist[i], angle, offset, precision)
    return polylist


def affineTransformationOfPolygon(polygon, angle, offset, precision):
    def pointTrafo(p):
        return affineTransformation(p, angle, offset, precision)

    # apply transformation on each point in the polygon (each line in the numpyArray)
    transformedPolygon = np.apply_along_axis(pointTrafo, 1, polygon)
    return transformedPolygon


def affineTransformation(point, angle, offset, precision):
    c = math.cos(math.radians(angle))
    s = math.sin(math.radians(angle))
    rotateMatrix = np.array([[c, -s], [s, c]])
    p = np.dot(rotateMatrix, point)
    p += offset
    p = np.round(p, precision)
    return p


def generateFoVWedge(
    openingAngle, baserange, radiusFactor, numberOfPointsOnCircle, directionAngle=0, offset=np.array([0, 0])
):
    """
    openingAngle: angle in degree < 180
    baserange: range a triangular shaped fov would have
    radiusFactor: the radius of the circle on top of the triangle (halfwidth (=0) <= radius <= baserange (=0))
    numberOfPointsOnCircle: resolution of the circle"""

    if numberOfPointsOnCircle < 0:
        raise Exception("Number of points on Circle must be > 0.")

    if (openingAngle < 0) or (openingAngle >= 180):
        raise Exception("Opening angle not in range from 0 to 180 degree.")

    origin = np.array([0, 0])
    # initialize fov polygon
    fov = np.array([origin])
    # calculate directions
    direction = np.array([0, 1])
    direction = direction / np.linalg.norm(direction)  # norm direction vector
    rotatePlus90Deg = np.array([[0, -1], [1, 0]])
    # pointing towards the left point direction
    leftPdir = np.dot(rotatePlus90Deg, direction)
    # calculate points
    midP = baserange * direction  # scale vector
    halfwidth = baserange * math.sin(math.radians(openingAngle / 2))  # of wedge
    leftP = midP + halfwidth * leftPdir
    rightP = midP - halfwidth * leftPdir
    # calculate the radius
    radius = halfwidth + radiusFactor * (baserange - halfwidth)
    # calculate center point of circle sector
    # c_y = leftP_y - sqrt(radius²-leftP_x²)
    center_y = leftP[1] - math.sqrt(radius ** 2 - leftP[0] ** 2)
    center = np.array([0, center_y])
    # calculate angle of circle sector
    circleSectorAngle = 2 * math.asin(halfwidth / radius)  # in radians
    if numberOfPointsOnCircle == 0:
        # we only have a triangle (without a circle on top)
        # add left point
        fov = np.append(fov, origin + np.array([leftP]), axis=0)
        # add right point
        fov = np.append(fov, origin + np.array([rightP]), axis=0)
    else:
        # increment numberOfPointsOnCircle by 1, so that it matches the actual number of points on circle without the two edges
        numberOfPointsOnCircle += 1
        circleSectorAngleDelta = circleSectorAngle / numberOfPointsOnCircle
        # init tempAngle
        # tempAngle = 0.0
        # init radius vector
        radiusvec = leftP - center
        # tempRadiusvec = radiusvec
        c = math.cos(-circleSectorAngleDelta)
        s = math.sin(-circleSectorAngleDelta)
        rotateMatrix = np.array([[c, -s], [s, c]])
        # add points to polygon
        for _ in range(0, numberOfPointsOnCircle + 1):
            tempPoint = origin + center + radiusvec
            # add point to fov
            fov = np.append(fov, np.array([tempPoint]), axis=0)
            # calculate next point
            radiusvec = np.dot(rotateMatrix, radiusvec)

    return affineTransformationOfPolygon(fov, directionAngle, offset, precision)


def generateCircle():
    pass


def generateRectangle():
    pass


def generateTriangle():
    pass


def generateWall():
    pass


def generatePolygonPatchCollection(listOfNumpyPolygons, colorV="blue", alphaV=0.4):
    polygons = []
    for p in listOfNumpyPolygons:
        polygons.append(Polygon(p, True))

    return PatchCollection(polygons, alpha=alphaV, color=colorV)


def main():
    # plotting
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # ax.autoscale_view()
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect("equal")
    plt.autoscale(False)
    plt.grid()
    plt.show()


def testCar():
    # initialization car
    fov1 = np.round(generateFoVWedge(60, 10, 0.7, 1, 0), precision)
    fov2 = np.round(generateFoVWedge(140, 4, 0.9, 1, 180), precision)
    # fov = [fov1, fov2]
    fov = [fov1]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array([[-1, 5], [2, 5], [1, 8]])
    p2 = np.array([[-5, 5], [-3, 5], [-3, 3], [-5, 3]])
    p3 = np.array([[-2.2, -3.8], [-0.8, -2.2], [-1.5, -6], [-2.5, -4.5], [-3, -3]])
    obs = [p1, p2, p3]

    # plotting
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # TODO: Bug detected! try 10,15,20 degree here # try to increase precision!
    car.updateCarPose(np.array([0, 0]), 125)  # 17.8

    print((car.fieldOfView))

    # # plot visible area
    visA = car.getVisibleArea(obs)
    # # # fovPatchCol = generatePolygonPatchCollection(visA)
    # # # ax.add_collection(fovPatchCol)

    visAPatchCol = generatePolygonPatchCollection(visA[1])
    visAPatchCol.set_color("green")
    ax.add_collection(visAPatchCol)

    visAPatchCol = generatePolygonPatchCollection(visA[2])
    visAPatchCol.set_color("green")
    ax.add_collection(visAPatchCol)

    # visAPatchCol = generatePolygonPatchCollection(visA[3])
    # visAPatchCol.set_color('green')
    # ax.add_collection(visAPatchCol)

    # visAPatchCol = generatePolygonPatchCollection(visA[4])
    # visAPatchCol.set_color('yellow')
    # ax.add_collection(visAPatchCol)

    visAPatchCol = generatePolygonPatchCollection(visA[5])
    visAPatchCol.set_color("yellow")
    ax.add_collection(visAPatchCol)

    visAPatchCol = generatePolygonPatchCollection(visA[7], "blue", 0.4)
    visAPatchCol.set_color("blue")
    ax.add_collection(visAPatchCol)

    # # plot obstacles
    obsPatchCol = generatePolygonPatchCollection(obs, "red", 0.1)
    ax.add_collection(obsPatchCol)

    # ax.autoscale_view()
    ax.set_xlim(-17, 17)
    ax.set_ylim(-17, 17)
    ax.set_aspect("equal")
    plt.autoscale(False)
    # plt.grid()
    plt.show()


def testFoVWedge():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    fov1 = generateFoVWedge(45, 10, 0.8, 20, 45)
    fov2 = generateFoVWedge(45, 10, 0.8, 20, -45)

    fovs = [fov1, fov2]

    fovs = affineTransformationOfPoylgonList(fovs, 90, 0, precision)

    fovPatchCol = generatePolygonPatchCollection(fovs)
    ax.add_collection(fovPatchCol)

    # ax.autoscale_view()
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_aspect("equal")
    plt.autoscale(False)
    plt.grid()
    plt.show()


def testAnimation():
    # plotting
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()

    # initialization car
    fov1 = generateFoVWedge(60, 10, 0.7, 20, 0)
    fov2 = generateFoVWedge(140, 4, 0.9, 20, 180)
    fov = [fov1, fov2]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array([[-1, 5], [2, 5], [1, 8]])
    p2 = np.array([[-5, 5], [-3, 5], [-3, 3], [-5, 3]])
    p3 = np.array([[-2.2, -3.8], [-0.8, -2.2], [-1.5, -6], [-2.5, -4.5], [-3, -3]])
    obs = [p1, p2, p3]

    # plot obstacles
    obsPatchCol = generatePolygonPatchCollection(obs, "red", 0.8)
    ax.add_collection(obsPatchCol)

    # visA = car.getVisibleArea(obs)
    # fovPatchCol = generatePolygonPatchCollection(visA)
    # ax.add_collection(fovPatchCol)

    def initAnimation():
        # ax.autoscale_view()
        # ax.set_xlim(-12, 12)
        # ax.set_ylim(-12, 12)
        ax.set_xlim(-17, 17)
        ax.set_ylim(-17, 17)
        ax.set_aspect("equal")
        plt.autoscale(False)

    def animate(frame):
        plt.cla()
        # ax.set_xlim(-12, 12)
        # ax.set_ylim(-12, 12)
        ax.set_xlim(-17, 17)
        ax.set_ylim(-17, 17)
        ax.set_aspect("equal")
        plt.autoscale(False)
        car.updateCarPose(np.array([0, 0]), math.radians(30))
        # plot obstacles
        obsPatchCol = generatePolygonPatchCollection(obs, "red", 0.8)
        ax.add_collection(obsPatchCol)
        # plot visible area
        visA = car.getVisibleArea(obs)
        # # # fovPatchCol = generatePolygonPatchCollection(visA)
        # # # ax.add_collection(fovPatchCol)
        if len(visA) == 8:
            # visAPatchCol = generatePolygonPatchCollection(visA[1])
            # visAPatchCol.set_color('green')
            # ax.add_collection(visAPatchCol)

            visAPatchCol = generatePolygonPatchCollection(visA[2])
            visAPatchCol.set_color("green")
            ax.add_collection(visAPatchCol)

            # visAPatchCol = generatePolygonPatchCollection(visA[3])
            # visAPatchCol.set_color('green')
            # ax.add_collection(visAPatchCol)

            # visAPatchCol = generatePolygonPatchCollection(visA[4])
            # visAPatchCol.set_color('yellow')
            # ax.add_collection(visAPatchCol)

            visAPatchCol = generatePolygonPatchCollection(visA[5])
            visAPatchCol.set_color("yellow")
            ax.add_collection(visAPatchCol)

            visAPatchCol = generatePolygonPatchCollection(visA[7], "blue", 0.4)
            visAPatchCol.set_color("blue")
            ax.add_collection(visAPatchCol)
        else:
            visAPatchCol = generatePolygonPatchCollection(visA[1], "blue", 0.4)
            visAPatchCol.set_color("blue")
            ax.add_collection(visAPatchCol)

    ani = FuncAnimation(
        fig, animate, frames=list(range(0, 100)), init_func=initAnimation, blit=False, repeat=True, interval=10
    )

    plt.show()


if __name__ == "__main__":
    # main()
    # testCar()
    # testFoVWedge()
    testAnimation()
