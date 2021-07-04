import numpy as np


def rotationMatrix(radian):
    c = np.cos(radian)
    s = np.sin(radian)
    return np.array([[c, -s], [s, c]])


def generateFoVWedge(fov_begin, fov_end, visible_range, heading=90, numberOfPointsOnCircle=15, origin=np.array([0, 0])):
    """
    openingAngle: angle in degree
    range: range of fov
    numberOfPointsOnCircle: resolution of the circle
    """

    # direction angle defined in VehicleSensorFOV
    directionAngle = 90

    # initialize fov polygon
    fov = np.array([origin])

    # angles of the circle approximation
    angles = np.linspace(
        (heading - directionAngle) + fov_begin,
        (heading - directionAngle) + fov_end,
        numberOfPointsOnCircle,
    )

    # first approx.
    rad = np.radians(angles[0])
    l = [np.cos(rad) * visible_range, np.sin(rad) * visible_range]

    # add points to polygon
    for a in angles:
        rotateMatrix = rotationMatrix(np.radians(a) - rad)
        tempPoint = np.dot(rotateMatrix, l) + origin
        # print "angle : ", a, " point : ", tempPoint, c, s
        fov = np.append(fov, np.array([tempPoint]), axis=0)

    return fov
