# This file is part of the Interpolated Polyline (https://github.com/...),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from p3iv_utils_polyline.interpolated_polyline import InterpolatedPolyline


class CoordinateTransform(object):
    def __init__(self, centerline_):
        assert isinstance(centerline_, np.ndarray)
        assert centerline_.shape[-1] == 2
        self.centerline = centerline_
        self.ip = InterpolatedPolyline(centerline_[:, 0], centerline_[:, 1])

    def xy2ld(self, input_coordinates):
        """
        Cartesian -> Frenet
        """
        return self._iterator(input_coordinates, self.ip.match)

    def ld2xy(self, input_coordinates):
        """
        Frenet -> Cartesian
        """
        return self._iterator(input_coordinates, self.ip.reconstruct)

    def expand(self, cartesian_position, longitudinal_position_arr, ignore_lateral_offset=False):
        """
        Given a motion profile in arc-length-coordinates, expand the dimension and transform it to Cartesian.

        Arguments
        ---------
        cartesian_position: np.ndarray
            Initial Cartesian coordinates [x, y]
        longitudinal_position_arr: np.ndarray
            Logitudinal position array
        ignore_lateral_offset: bool
            Flag to ignore current lateral offset
        """

        # typecast if list
        longitudinal_position_arr = np.asarray(longitudinal_position_arr)

        offset_l, offset_d = self.xy2ld(cartesian_position)
        ld_array = np.zeros([len(longitudinal_position_arr), 2])
        ld_array[:, 0] = longitudinal_position_arr + offset_l
        if not ignore_lateral_offset:
            ld_array[:, 1] = np.linspace(offset_d, 0.0, len(longitudinal_position_arr))
        return self.ld2xy(ld_array)

    @staticmethod
    def _iterator(input_coordinates, func):

        input_coordinates = np.asarray(input_coordinates)

        flag = False
        if len(input_coordinates.shape) is 1:
            input_coordinates = input_coordinates.reshape(-1, 2)
            flag = True

        output_coordinates = np.empty((len(input_coordinates), 2))
        for i in range(len(input_coordinates)):
            output_coordinates[i] = func(input_coordinates[i, 0], input_coordinates[i, 1])

        if flag:
            # Reshape to (2, )
            return output_coordinates[0]
        else:
            return output_coordinates


if __name__ == "__main__":
    centerline = np.zeros([10, 2])
    centerline[:, 0] = np.arange(10)
    centerline[:, 1] = np.arange(10)
    c = CoordinateTransform(centerline)
    xy_0 = [4.0, 0.0]
    ld_0 = c.xy2ld(xy_0)
    xy_1 = [4.0, 8.0]
    ld_1 = c.xy2ld(xy_1)
    print("ld_0 : ")
    print(ld_0)
    print("ld_1 : ")
    print(ld_1)
