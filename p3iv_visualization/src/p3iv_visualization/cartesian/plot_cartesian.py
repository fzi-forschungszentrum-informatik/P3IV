from __future__ import division
import os
from collections import OrderedDict
from p3iv_visualization.lanelet2.plot_map import PlotLanelet2Map
from p3iv_visualization.cartesian.plot_vehicle import PlotVehicle


class PlotCartesian(object):
    def __init__(self, ax, lanelet_map_file, center_vehicle_id=None, imagery_data=None, plot_uncertainty_ellipse=True):
        self.ax = ax
        self.center_vehicle_id = center_vehicle_id
        self.uncertainty = plot_uncertainty_ellipse
        self.map_plot = PlotLanelet2Map(self.ax, lanelet_map_file, imagery_data=imagery_data)
        self.vehicles = OrderedDict()

    def plot_buildings(self):
        # todo
        pass

    def fill_vehicles(self, vehicles):
        for v in vehicles:
            self.vehicles[v.id] = PlotVehicle(
                self.ax, v.id, v.appearance.color, car_width=v.appearance.width, car_length=v.appearance.length
            )

    def set_vehicle_plots(self):
        path_file = os.path.dirname(os.path.realpath(__file__))
        path_img = os.path.normpath(os.path.join(path_file, "../res/car.png"))

        for vehicle_id, pv in self.vehicles.items():

            if vehicle_id == self.center_vehicle_id:
                # do not try to set these for other vehicles;
                # PlotVehicle() takes self.ax as arg and PlotVehicle modifies self.ax!
                pv.create_track()
                pv.set_visible_area()
                pv.set_car_image(path_img)
            else:
                pv.set_car_patch()

            if self.uncertainty:
                pv.set_uncertainty_ellipse()

    def update_vehicle_plot(
        self,
        vehicle_id,
        x,
        y,
        yaw,
        speed,
        uncertainty_ellipses=None,  # np.asarray([ellipse_inner_width, ellipse_inner_height])
        visible_region=None,
        motion_past=None,
        motion_future=None,
        zoom=30,
        set_facecolor=True,
    ):

        pv = self.vehicles[vehicle_id]

        if vehicle_id == self.center_vehicle_id:
            pv.center_vehicle_in_plot(x, y, zoom)
            pv.update_car_image(x, y, yaw)

            if visible_region is not None:
                pv.update_visible_area(visible_region)

            if motion_past is not None and motion_future is not None:
                pv.update_track(motion_past, motion_future)

        else:
            pv.update_car_patch_center(x, y, yaw, set_facecolor=set_facecolor)

        if self.uncertainty and uncertainty_ellipses is not None:
            pv.update_uncertainty_ellipse(x, y, yaw, uncertainty_ellipses)

        pv.update_speed_info_text(x, y, speed)
