import numpy as np
import lanelet2.geometry
from lanelet2.core import BasicPoint2d, LaneletSequence
from lanelet2.geometry import ArcCoordinates


class CoordinateTransform(object):
    def __init__(self, centerline):
        if isinstance(centerline, (np.ndarray, list)):
            if isinstance(centerline[0], (lanelet2.core.Lanelet, lanelet2.core.ConstLanelet)):
                llt_sq = LaneletSequence(centerline)
                self._centerline = lanelet2.geometry.to2D(llt_sq.centerline)
            elif isinstance(centerline[0], (np.ndarray, list)):
                # create a linestring from Cartesian points
                points = []
                for i, xy in enumerate(centerline):
                    points.append(lanelet2.core.Point3d(i, xy[0], xy[1], 0.0))
                ls = lanelet2.core.LineString3d(0, points)
                self._centerline = lanelet2.geometry.to2D(ls)
            else:
                raise TypeError
        elif isinstance(centerline, (lanelet2.core.LineString3d, lanelet2.core.ConstLineString3d)):
            self._centerline = lanelet2.geometry.to2D(llt_sq.centerline)
        elif isinstance(centerline, (lanelet2.core.LineString2d, lanelet2.core.ConstLineString2d)):
            self._centerline = centerline
        else:
            raise TypeError

    def iterate(func):
        def wrapper(self, input_coordinates):
            input_coordinates = np.asarray(input_coordinates)

            flag = False
            if len(input_coordinates.shape) is 1:
                input_coordinates = input_coordinates.reshape(-1, 2)
                flag = True

            output_coordinates = func(self, input_coordinates)

            if flag:
                # Reshape to (2, )
                return output_coordinates[0]
            else:
                return output_coordinates

        return wrapper

    @iterate
    def xy2ld(self, input_coordinates):
        """
        Cartesian -> Frenet
        """
        output_coordinates = np.empty((len(input_coordinates), 2))
        for i in range(len(input_coordinates)):
            frenet = lanelet2.geometry.toArcCoordinates(
                self._centerline, self._convert2basicPoint2d(input_coordinates[i])
            )
            output_coordinates[i] = np.asarray([frenet.length, frenet.distance])
        return output_coordinates

    @iterate
    def ld2xy(self, input_coordinates):
        """
        Frenet -> Cartesian
        """
        output_coordinates = np.empty((len(input_coordinates), 2))
        for i in range(len(input_coordinates)):
            cartesian = lanelet2.geometry.fromArcCoordinates(
                self._centerline, self._convert2arcCoordinates(input_coordinates[i])
            )
            output_coordinates[i] = np.asarray([cartesian.x, cartesian.y])
        return output_coordinates

    def expand(self, cartesian_position, longitudinal_position_arr):

        """
        Given a motion profile in arc-length-coordinates, expand the dimension and transform it to Cartesian.

        Arguments
        ---------
        cartesian_position: np.ndarray
            Initial Cartesian coordinates [x, y]
        longitudinal_position_arr: np.ndarray
            Logitudinal position array
        """

        # typecast if list
        longitudinal_position_arr = np.asarray(longitudinal_position_arr)

        offset_l, offset_d = self.xy2ld(cartesian_position)
        ld_array = np.empty([len(longitudinal_position_arr), 2])
        ld_array[:, 0] = longitudinal_position_arr + offset_l
        ld_array[:, 1] = np.linspace(offset_d, 0.0, len(longitudinal_position_arr))
        return self.ld2xy(ld_array)

    @staticmethod
    def _convert2basicPoint2d(input_coordinates):
        """
        Typecasting for Lanelet2.
        """
        cartesian = lanelet2.core.BasicPoint2d()
        cartesian.x, cartesian.y = input_coordinates
        return cartesian

    @staticmethod
    def _convert2arcCoordinates(input_coordinates):
        """
        Typecasting for Lanelet2.
        """
        frenet = lanelet2.geometry.ArcCoordinates()
        frenet.length, frenet.distance = input_coordinates
        return frenet
