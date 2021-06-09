# This file is part of the Interpolated Polyline (https://github.com/...),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from __future__ import division
import numpy as np
import time
from matplotlib import pyplot as plt


def create_mesh(r, offset=2.0, K=1):
    """
    :param r: 2D-numpy array of the reference line
    :param offset: offset added to plot the contours
    :return: 2d meshgrid
    """

    min_x, max_x = np.min(r[:, 0]), np.max(r[:, 0])
    min_y, max_y = np.min(r[:, 1]), np.max(r[:, 1])

    print("min_x, max_x")
    print(min_x, max_x)
    print("min_y, max_y")
    print(min_y, max_y)

    x_val = np.linspace(min_x - offset, max_x + offset, 10 * K)
    y_val = np.linspace(min_y - offset, max_y + offset, 10 * K)
    mesh_x, mesh_y = np.meshgrid(x_val, y_val)
    return [x_val, y_val, mesh_x, mesh_y]


def distance_and_gradient_of_mesh(mesh_x, mesh_y, polyline_obj, distance_bound=1e6):

    # Get the shape specifications of x
    row, column = mesh_x.shape

    # Initialize an empty array
    mesh_z = np.zeros(shape=(row, column))
    mesh_t = np.zeros(shape=(row, column))

    t_start = time.time()
    for r in range(row):
        for c in range(column):
            d, dtheta = polyline_obj.tangent(mesh_x[r, c], mesh_y[r, c])
            mesh_z[r, c] = np.clip(d, -distance_bound, distance_bound)
            mesh_t[r, c] = dtheta
    t_end = time.time()

    nr_entries = row * column
    print("Duration of calculating {} distance entries".format(nr_entries))
    print(t_end - t_start)
    return mesh_z, mesh_t


def plot_meshgrid(ax, mesh_x, mesh_y, mesh_z, K=1):

    # Get the highest value of the function
    upper_bound = np.ceil(max([max(abs(element)) for element in mesh_z]))
    print("upper bound {}".format(upper_bound))
    print("-upper bound {}".format(-upper_bound))

    # Define the number of levels of contour-map
    levels = np.linspace(-upper_bound, upper_bound, 50)

    # Plot the contour-map
    cs = ax.contourf(mesh_x, mesh_y, mesh_z, levels=levels)

    # Add a colorbar to the figure
    cbar = plt.colorbar(cs)


def set_axis_limits(ax, x_val, y_val):
    ax.set_xlim(np.min(x_val), np.max(x_val))
    ax.set_ylim(np.min(y_val), np.max(y_val))


def plot_reference_line(ax, r):
    """
    :param r: 2D-numpy array of the reference line
    :return:
    """
    ax.plot(r[:, 0], r[:, 1], "b")


def instantiate_plot():
    fig = plt.figure("Interpolated Polyline Function")
    ax = fig.add_subplot(111)

    # ax.grid()
    ax.set_aspect("equal")
    return ax
