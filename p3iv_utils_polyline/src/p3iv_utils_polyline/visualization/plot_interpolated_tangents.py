# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from p3iv_utils_polyline.visualization.utils import *


def main(r, polyline_obj, offset, K_mesh, distance_bounds, K_arrows, show=True):
    ax = instantiate_plot()
    x_val, y_val, mesh_x, mesh_y = create_mesh(oo, offset=offset, K=K_mesh)
    set_axis_limits(ax, x_val, y_val)
    mesh_z1, mesh_t = distance_and_gradient_of_mesh(mesh_x, mesh_y, polyline_obj, distance_bound=distance_bounds)

    plot_reference_line(ax, oo)
    plot_meshgrid(ax, mesh_x, mesh_y, mesh_z1)

    K_arrows = 10
    ax.quiver(
        x_val[::K_arrows],
        y_val[::K_arrows],
        np.cos(mesh_t)[::K_arrows, ::K_arrows],
        np.sin(mesh_t)[::K_arrows, ::K_arrows],
        pivot="tail",
    )

    ax.scatter(mesh_x[::K_arrows, ::K_arrows], mesh_y[::K_arrows, ::K_arrows], color="black", s=5)

    if show:
        plt.show()


if __name__ == "__main__":
    import numpy as np
    from p3iv_utils_polyline.py_interpolated_polyline import PyInterpolatedPolyline as InterpolatedPolyline
    from p3iv_utils_polyline.interpolated_polyline import InterpolatedPolyline

    """
    oo = np.array([[-0.5, -0.5], [0.0, 0.0], [0.3,  -0.4], [0.6,  0.0],
                [1.2, -0.5], [1.7,  0.0], [2.2,  -0.5]])

    """
    oo = np.array(
        [[0.0, 0.0], [0.4, -0.3], [1.0, -0.6], [2.0, -1.0], [3.0, -1.0], [3.5, -0.8], [4.5, -0.5], [5.5, 0.5]]
    )

    polyline_obj = InterpolatedPolyline(oo[:, 0], oo[:, 1])

    offset = 1.0
    K_mesh = 20
    distance_bounds = 2.0
    K_arrows = 10
    main(oo, polyline_obj, offset, K_mesh, distance_bounds, K_arrows)
