from __future__ import division, absolute_import
import numpy as np
import math

import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection
from p3iv_utils_polyvision_pyapi.pypolyvision import VisibleArea, checkInside
from p3iv_utils_polyvision.fov_wedge import generateFoVWedge

precision = 6


class Car(object):
    """
    A Car
    """

    def __init__(self, fieldOfViewContour, position, yawAngle):
        self._fieldOfView = fieldOfViewContour
        self._position = np.array([0, 0])
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
        visA = VisibleArea(self._position, self._fieldOfView, perceptedPolygons)
        # calculate visible area
        visA.calculateVisibleArea()
        results = [visA.getFieldsOfView(), visA.getOpaquePolygons(), visA.getVisibleAreas(), visA.getNonVisibleAreas()]
        return results

    def getVisibilityBorder(self, perceptedPolygons, centerline):
        # create visibleArea object for calculations
        visA = VisibleArea(self._position, self._fieldOfView, perceptedPolygons)
        # calculate visible area
        return visA.getVisibilityBorder(centerline)


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


def testFoVWedge():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    opening_angle = 90
    visible_range = 4
    fov1 = generateFoVWedge(opening_angle, visible_range, directionAngle=90)
    fov2 = generateFoVWedge(135, 2, directionAngle=270)
    fovs = [fov1, fov2]

    fovPatchCol = generatePolygonPatchCollection(fovs)
    ax.add_collection(fovPatchCol)

    print checkInside(np.array([0, 2]), [fov1])

    # ax.autoscale_view()
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_aspect("equal")
    plt.autoscale(False)
    plt.grid()
    plt.show()


def testVisualisation0():
    origin = np.array([0, 0])
    fov1 = np.array([[0, 0], [-4, 10], [4, 10]])
    fov2 = np.array([[0, 0], [-6, -4], [6, -4]])
    fov = [fov1, fov2]
    obs1 = np.array([[-1, 5], [1, 5], [0, 7]])

    # obs1 = np.array([[-3, 5],
    #                  [-0.5, 5],
    #                  [-1, 7]])

    # obs1 = np.array([[-3, 5],
    #                  [-1, 5],
    #                  [-2, 7]])
    obs1 = obs1 + np.array([0, 0])
    obs = [obs1]
    # obs = []
    # plot results
    car = Car(fov, origin, 0)
    genericTestPlot(obs, car)


def testVisualisation1():
    # initialization car
    fov1 = generateFoVWedge(40, 10, directionAngle=0)
    fov2 = generateFoVWedge(140, 4, directionAngle=180)
    fov3 = generateFoVWedge(25, 7, directionAngle=-30)
    fov4 = generateFoVWedge(25, 7, directionAngle=30)
    fov5 = generateFoVWedge(40, 7, directionAngle=180)
    fov = [fov1, fov2, fov3, fov4, fov5]
    car = Car(fov, np.array([0, 0]), 0)
    car.updateCarPose(np.array([0, 0]), -90)

    # initialization obstacles
    p1 = np.array([[-1, 5], [1, 5], [0, 8]])
    p2 = np.array([[-5, 5], [-3, 5], [-3, 3], [-5, 3]])
    p3 = np.array([[-2.2, -3.8], [-0.8, -2.2], [-1.5, -6], [-2.5, -4.5], [-3, -3]])
    p4 = np.array(
        [
            [8, 4],
            [8, 2],
            [5, 0],
            [10, 1],
            [9.333333, 0],  # this is the intersection point
            [8, -2],
            [7, -4],
            [11, -1],
            [11, 2],
        ]
    )
    p5 = np.array([[-4, 0], [-6, 0], [-6, -1.5]])
    obs = [p1, p2, p3, p4, p5]

    # plot results
    genericTestPlot(obs, car)


def testVisualisation2Shadowing():
    # initialize car
    fov1 = np.array([[0, 0], [2, 12], [14, 8], [14, -8], [2, -12]])
    fov = [fov1]
    car = Car(fov, np.array([0, 0]), 0)
    car.updateCarPose(np.array([0, 0]), 0)

    # initialize obs
    p1 = np.array(
        [[2, 7], [6, 3], [2, 5], [2, 1], [4, 3], [4, -2], [2, -1], [2, -4], [7, -1], [2, -8], [9, -8], [9, 7]]
    )
    obs = [p1]

    # plot results
    genericTestPlot(obs, car)


def testVisualisation3():
    # initialize car
    fov1 = np.array([[0, 0], [2, 12], [14, 8], [14, -8], [2, -12]])
    fov = [fov1]
    car = Car(fov, np.array([0, 0]), 0)
    car.updateCarPose(np.array([0, 0]), 0)

    # initialize obs
    p1 = np.array(
        [
            [2, 3],
            [3, 3],
            [3, 4],
            [3, 6],
            [5, 6],
            [6, 6],
            [6, 3],
            [6, 0],
            [6, -2],
            [4, -2],
            [3, -2],
            [3, 1],
            [2, 1],
            [2, -3],
            [7, -3],
            [7, 7],
            [2, 7],
        ]
    )
    # p1 = affineTransformationOfPolygon(p1,0,np.array([0,-2]),precision)
    obs = [p1]

    # plot results
    genericTestPlot(obs, car)


def testVisualisation4OriginInsideNonConvexPoly():

    # fov1 = generateFoVWedge(40, 10, 0.7, 20, 0)
    # fov2 = generateFoVWedge(140, 4, 0.9, 20, 180)
    # fov3 = generateFoVWedge(25, 7, 0.7, 10, -30)
    # fov4 = generateFoVWedge(25, 7, 0.7, 10, 30)
    # fov5 = generateFoVWedge(40, 7, 0.7, 20, 180)
    # fov = [fov1, fov2, fov3, fov4, fov5]
    fov1 = generateFoVWedge(50, 10, 0.7, 1)
    fov = [fov1]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array(
        [
            [2, 3],
            [3, 3],
            [3, 4],
            [3, 6],
            [5, 6],
            [6, 6],
            [6, 3],
            [6, 0],
            [6, -2],
            [4, -2],
            [3, -2],
            [3, 1],
            [2, 1],
            [2, -3],
            [7, -3],
            [7, 7],
            [2, 7],
        ]
    )
    p1 = affineTransformationOfPolygon(p1, 0, np.array([-4, -2]), precision)
    obs = [p1]

    # plot results
    genericTestPlot(obs, car)


def testVisualisation5OriginInsideNonConvexPoly():
    # initialization car
    fov1 = generateFoVWedge(50, 10, 0.7, 1)
    fov = [fov1]
    car = Car(fov, np.array([0, 0]), 0)
    # initialization obstacles
    p1 = np.array([[-4, 0], [-5, 3], [1, 6], [6, 3], [0, -3], [-2, -3], [-2, -2], [-1, -2], [2, 2], [-1, 2]])
    p1 = affineTransformationOfPolygon(p1, 0, np.array([0, 0]), precision)
    obs = [p1]

    # plot results
    genericTestPlot(obs, car)


def testVisualisation6OriginInsideNonConvexPoly():
    # initialization car
    fov1 = generateFoVWedge(50, 10, 0.7, 1)
    fov = [fov1]
    car = Car(fov, np.array([0, 0]), 0)
    # initialization obstacles
    p1 = np.array([[-1, 2], [-4, 0], [-5, 3], [1, 6], [6, 3], [0, -3], [-2, -3], [-4, -1], [-1, -2], [2, 2]])
    p1 = affineTransformationOfPolygon(p1, 0, np.array([0, 0]), precision)
    obs = [p1]

    # plot results
    genericTestPlot(obs, car)


def testVisualisation7OriginInsideObstacle():
    origin = np.array([0, 0])
    fov1 = np.array([[0, 0], [-4, 10], [4, 10]])
    fov2 = np.array([[0, 0], [-6, -4], [6, -4]])
    fov = [fov1, fov2]
    obs1 = np.array([[-1, 5], [1, 5], [0, -7]])

    obs = [obs1]
    # plot results
    car = Car(fov, origin, 0)
    genericTestPlot(obs, car)


def testVisualisation8OriginOutsideFov():
    origin = np.array([0, 0])
    fov1 = np.array([[0, 3], [-4, 10], [4, 10]])
    # fov2 = np.array([[0, 0],
    #                  [-6, -4],
    #                  [6, -4]])
    # fov = [fov1, fov2]
    fov = [fov1]
    obs1 = np.array([[-1, 5], [1, 5], [0, 7]])

    obs = [obs1]
    # plot results
    car = Car(fov, origin, 0)
    genericTestPlot(obs, car)


def testVisualisation9EmptyFov():
    origin = np.array([0, 0])
    fov = []
    obs1 = np.array([[-1, 5], [1, 5], [0, 7]])

    obs = [obs1]
    # plot results
    car = Car(fov, origin, 0)
    genericTestPlot(obs, car)


def testAnimation1():
    # initialization car
    fov1 = generateFoVWedge(40, 10, directionAngle=0)
    fov2 = generateFoVWedge(140, 4, directionAngle=180)
    fov3 = generateFoVWedge(25, 7, directionAngle=-30)
    fov4 = generateFoVWedge(25, 7, directionAngle=30)
    fov5 = generateFoVWedge(40, 7, directionAngle=180)
    fov = [fov1, fov2, fov3, fov4, fov5]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array([[-1, 5], [1, 5], [0, 8]])
    p2 = np.array([[-5, 5], [-3, 5], [-3, 3], [-5, 3]])
    p3 = np.array([[-2.2, -3.8], [-0.8, -2.2], [-1.5, -6], [-2.5, -4.5], [-3, -3]])
    p4 = np.array([[8, 4], [8, 2], [5, 0], [10, 1], [8, -2], [7, -4], [11, -1], [11, 2]])
    p5 = np.array([[-4, 0], [-6, 0], [-6, -1.5]])
    obs = [p1, p2, p3, p4, p5]
    genericTestAnimation(obs, car)


def testLine():
    # initialization car
    fov1 = generateFoVWedge(40, 10, directionAngle=0)
    fov2 = generateFoVWedge(140, 4, directionAngle=180)
    fov3 = generateFoVWedge(25, 7, directionAngle=-30)
    fov4 = generateFoVWedge(25, 7, directionAngle=30)
    fov5 = generateFoVWedge(40, 7, directionAngle=180)
    fov = [fov1, fov2, fov3, fov4, fov5]
    car = Car(fov, np.array([0, 0]), 0)
    obs = []
    line = np.array([12.0, 0.0, 5.0, 0.0])
    genericTestLinePlot(obs, car, line)


def testAnimation2Shadowing():
    # initialization car
    fov1 = generateFoVWedge(40, 10, 0.7, 20, 0)
    fov2 = generateFoVWedge(140, 4, 0.9, 20, 180)
    fov3 = generateFoVWedge(25, 7, 0.7, 10, -30)
    fov4 = generateFoVWedge(25, 7, 0.7, 10, 30)
    fov5 = generateFoVWedge(40, 7, 0.7, 20, 180)
    fov = [fov1, fov2, fov3, fov4, fov5]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array(
        [[2, 7], [6, 3], [2, 5], [2, 1], [4, 3], [4, -2], [2, -1], [2, -4], [7, -1], [2, -8], [9, -8], [9, 7]]
    )
    p2 = np.copy(p1)
    p2[:, 0] *= -1
    obs = [p1, p2]
    genericTestAnimation(obs, car)


def testAnimation3():
    # initialization car
    fov1 = generateFoVWedge(40, 10, 0.7, 20, 0)
    fov2 = generateFoVWedge(140, 4, 0.9, 20, 180)
    fov3 = generateFoVWedge(25, 7, 0.7, 10, -30)
    fov4 = generateFoVWedge(25, 7, 0.7, 10, 30)
    fov5 = generateFoVWedge(40, 7, 0.7, 20, 180)
    fov = [fov1, fov2, fov3, fov4, fov5]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array(
        [
            [2, 3],
            [3, 3],
            [3, 4],
            [3, 6],
            [5, 6],
            [6, 6],
            [6, 3],
            [6, 0],
            [6, -2],
            [4, -2],
            [3, -2],
            [3, 1],
            [2, 1],
            [2, -3],
            [7, -3],
            [7, 7],
            [2, 7],
        ]
    )
    p1 = affineTransformationOfPolygon(p1, 0, np.array([0, -2]), precision)
    obs = [p1]
    genericTestAnimation(obs, car)


def testAnimation4():
    # initialization car
    fov1 = generateFoVWedge(40, 10, directionAngle=20)
    fov2 = generateFoVWedge(140, 4, directionAngle=20)
    fov3 = generateFoVWedge(25, 7, directionAngle=10)
    fov4 = generateFoVWedge(25, 7, directionAngle=10)
    fov5 = generateFoVWedge(40, 7, directionAngle=20)
    fov = [fov1, fov2, fov3, fov4, fov5]
    car = Car(fov, np.array([0, 0]), 0)

    # initialization obstacles
    p1 = np.array(
        [
            [2, 3],
            [3, 3],
            [3, 4],
            [3, 6],
            [5, 6],
            [6, 6],
            [6, 3],
            [6, 0],
            [6, -2],
            [4, -2],
            [3, -2],
            [3, 1],
            [2, 1],
            [2, -3],
            [7, -3],
            [7, 7],
            [2, 7],
        ]
    )
    p1 = affineTransformationOfPolygon(p1, 0, np.array([-4, -2]), precision)
    obs = [p1]
    genericTestAnimation(obs, car)


def genericTestLinePlot(obstacles, car, line):
    # plotting
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()

    plt.cla()
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    # ax.set_xlim(-17, 17)
    # ax.set_ylim(-17, 17)
    ax.set_aspect("equal")
    plt.autoscale(False)
    car.updateCarPose(np.array([0, 0]), math.radians(30))

    # get visible area calculation results
    visA = car.getVisibleArea(obstacles)

    # plot obstacles
    obsPatchCol = generatePolygonPatchCollection(visA[1], "red", 0.8)
    ax.add_collection(obsPatchCol)

    # plot visible area
    visAreaPatchCol = generatePolygonPatchCollection(visA[2], "blue", 0.4)
    ax.add_collection(visAreaPatchCol)

    # plot boundary of visible area with a centerline
    print ("Line-point coordinates")
    intersection = car.getVisibilityBorder(obstacles, line)[0]
    print (intersection)
    ax.plot([line[0], line[2]], [line[1], line[3]])
    ax.plot(intersection[0], intersection[1], "o", ms=8)

    # plot non-visible area
    visAreaPatchCol = generatePolygonPatchCollection(visA[3], "grey", 0.4)
    ax.add_collection(visAreaPatchCol)

    plt.show()


def genericTestAnimation(obstacles, car):
    # plotting
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()

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
        ax.set_xlim(-12, 12)
        ax.set_ylim(-12, 12)
        # ax.set_xlim(-17, 17)
        # ax.set_ylim(-17, 17)
        ax.set_aspect("equal")
        plt.autoscale(False)
        car.updateCarPose(np.array([0, 0]), math.radians(30))

        # get visible area calculation results
        visA = car.getVisibleArea(obstacles)

        # plot obstacles
        obsPatchCol = generatePolygonPatchCollection(visA[1], "red", 0.8)
        ax.add_collection(obsPatchCol)

        # plot visible area
        visAreaPatchCol = generatePolygonPatchCollection(visA[2], "blue", 0.4)
        ax.add_collection(visAreaPatchCol)

        # plot non-visible area
        visAreaPatchCol = generatePolygonPatchCollection(visA[3], "grey", 0.4)
        ax.add_collection(visAreaPatchCol)

    ani = FuncAnimation(
        fig, animate, frames=range(0, 100), init_func=initAnimation, blit=False, repeat=True, interval=10
    )

    plt.show()


def genericTestPlot(obstacles, car):
    # plotting
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    import time

    start_time = time.time()
    # get visible area calculation results
    visAList = car.getVisibleArea(obstacles)
    print ("--- %s seconds ---" % (time.time() - start_time))

    # plot obstacles
    obsPatchCol = generatePolygonPatchCollection(visAList[1], "red", 0.8)
    ax.add_collection(obsPatchCol)

    # plot visible area
    visAreaPatchCol = generatePolygonPatchCollection(visAList[2], "blue", 0.4)
    ax.add_collection(visAreaPatchCol)

    # plot non-visible area
    visAreaPatchCol = generatePolygonPatchCollection(visAList[3], "grey", 0.4)
    ax.add_collection(visAreaPatchCol)

    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    # ax.set_xlim(-17, 17)
    # ax.set_ylim(-17, 17)
    ax.set_aspect("equal")
    plt.autoscale(False)
    plt.show()


# plot with central projected polygons


def genericTestPlot2(obstacles, car):
    # plotting
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    import time

    start_time = time.time()
    # get visible area calculation results
    visAList = car.getVisibleArea(obstacles)
    print ("--- %s seconds ---" % (time.time() - start_time))

    # plot obstacles
    obsPatchCol = generatePolygonPatchCollection(visAList[1], "red", 0.8)
    ax.add_collection(obsPatchCol)

    # plot visible area
    visAreaPatchCol = generatePolygonPatchCollection(visAList[2], "green", 0.4)
    ax.add_collection(visAreaPatchCol)

    # plot field of view
    visAreaPatchCol = generatePolygonPatchCollection(visAList[0], "blue", 0.4)
    ax.add_collection(visAreaPatchCol)

    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    # ax.set_xlim(-1000000, 1000000)
    # ax.set_ylim(-1000000, 1000000)
    ax.set_aspect("equal")
    plt.autoscale(False)
    plt.show()


if __name__ == "__main__":
    # main()
    testFoVWedge()
    testLine()
    testAnimation1()
    # testAnimation2Shadowing()
    # testAnimation3()
    testAnimation4()
    # testVisualisation0()
    # testVisualisation1()
    # testVisualisation2Shadowing()
    # testVisualisation3()
    # testVisualisation4OriginInsideNonConvexPoly()
    # testVisualisation5OriginInsideNonConvexPoly()
    # testVisualisation6OriginInsideNonConvexPoly()
    # testVisualisation7OriginInsideObstacle()
    # testVisualisation8OriginOutsideFov()
    # testVisualisation9EmptyFov()
