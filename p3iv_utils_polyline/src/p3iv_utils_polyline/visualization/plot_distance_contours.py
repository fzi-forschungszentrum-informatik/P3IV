# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from p3iv_utils_polyline.visualization.utils import *


def main(r, polyline_obj, offset, distance_bound=50, show=True):
    _, _, mesh_x, mesh_y = create_mesh(r, offset=offset, K=20)
    mesh_z, _ = distance_and_gradient_of_mesh(mesh_x, mesh_y, polyline_obj, distance_bound=distance_bound)
    if show:
        ax = instantiate_plot()
        plot_reference_line(ax, r)
        plot_meshgrid(ax, mesh_x, mesh_y, mesh_z, K=1)
        plt.show()
