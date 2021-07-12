# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from p3iv_visualization.cartesian.plot_cartesian import PlotCartesian
from p3iv_visualization.spatiotemporal.utils.plot_utils import PlotUtils
from p3iv_visualization.spatiotemporal.utils.plot_ego_motion import PlotEgoMotion
from p3iv_visualization.spatiotemporal.utils.plot_other_vehicles import PlotOtherVehicles
from p3iv_visualization.motion.plot_motion_components import PlotMotionComponents
from p3iv_visualization.animations.animation_frame import AnimationFrame
from p3iv_utils.coordinate_transformation import CoordinateTransform
from p3iv_utils.vehicle_models import get_control_inputs


class Animator(object):
    def __init__(
        self,
        lanelet_map_file,
        map_coordinate_origin,
        vehicle_id,
        vehicle_color,
        vehicles,
        dt,
        imagery_data=None,
        header=None,
    ):
        a = AnimationFrame()
        if header:
            a.set_header(header)
        a.create_subplots()
        a.set_subplot_titles()
        a.set_buttons()
        self.frame = a

        self.dt = dt

        self.fig = a.fig
        self.ax0 = a.ax0
        self.ax1 = a.ax1
        self.ax2 = a.ax2
        self.ax3 = a.ax3
        self.ax4 = a.ax4

        self.vehicle_id = vehicle_id
        self.vehicle_color = vehicle_color
        self.timesteps = None
        self.n_pin_past = None
        self.n_pin_future = None

        self.p_ax0_pu = PlotUtils(ax=self.ax0)
        self.p_ax0_pov = PlotOtherVehicles(self.ax0, dt)
        self.p_ax0_pem = PlotEgoMotion(self.ax0, self.vehicle_id, self.vehicle_color)

        self.p_ax1 = PlotCartesian(
            self.ax1,
            lanelet_map_file,
            map_coordinate_origin,
            center_vehicle_id=self.vehicle_id,
            imagery_data=imagery_data,
        )
        self.p_ax1.fill_vehicles(vehicles)
        self.p_ax1.set_vehicle_plots()
        self.timestamp_text = self.ax1.text(0.65, 0.04, "", transform=self.ax1.transAxes, fontsize=8)

        self.p_ax234 = PlotMotionComponents(self.ax2, self.ax3, self.ax4)

    def init_spatiotemporal_plot(self, N, N_pin_past, N_pin_future):
        self.n_pin_past = N_pin_past
        self.n_pin_future = N_pin_future
        self.p_ax0_pu.set_settings(self.dt, N, None)
        self.p_ax0_pu.set_labels()
        self.p_ax0_pem.create_motion_profile(self.dt, N)
        self.p_ax0_pem.create_stop_positions()
        # self.p_ax0_pem.create_initial_position()
        self.p_ax0_pem.create_time_highlighter()

    def init_motion_profile(self, N, N_pin_past, N_pin_future):
        self.n_pin_past = N_pin_past
        self.n_pin_future = N_pin_future
        # N+1 because of the start point, which is already present
        self.timesteps = self.dt * np.arange(N + 1)
        self.p_ax234.initialize(self.timesteps)
        self.p_ax234.set_labels()

    def update_ego(self, timestampdata, i, magnitude_flag=False):
        # The plots on ax0 are 'static'

        # Path-time Diagram
        c = CoordinateTransform(timestampdata.decision_base.corridor.center)
        ld = c.xy2ld(timestampdata.plan_optimal.states.position.mean)

        # because l_current is subtrachted as offset, static axis limits can be attained
        longitudinal_pos = ld[:, 0] - ld[0, 0]
        self.p_ax0_pem.update_motion_profile(longitudinal_pos)
        # self.p_ax0_pem.update_stop_positions(motion_future, self.n_pin_future + 1)  # m. future contains the curr. pos
        # self.p_ax0_pem.update_initial_position(timestampdata.motion[-1])
        # self.p_ax0_pem.delete_motion_limits()
        # self.p_ax0_pem.plot_motion_limits(timestampdata.motion[-1])

        self.p_ax0_pu.set_axis_limits(-50.0, 100.0)
        self.p_ax0_pem.update_timelighter(i * self.dt)

        # Cartesian-Motion Diagram
        x, y = timestampdata.plan_optimal.states.position.mean[i]
        yaw = timestampdata.plan_optimal.states.yaw.mean[i]
        speed = timestampdata.plan_optimal.states.speed[i]
        visible_region = timestampdata.environment.visible_areas
        uncertainty_ellipse = None  # v.state.position[2:]

        self.p_ax1.update_vehicle_plot(
            self.vehicle_id,
            x,
            y,
            yaw,
            speed,
            visible_region=visible_region,
            zoom=self.frame.zoom,
            motion_past=timestampdata.plan_optimal.states.position.mean[: i + 1],
            motion_future=timestampdata.plan_optimal.states.position.mean[i:],
        )

        controls = get_control_inputs(
            timestampdata.plan_optimal.states.yaw.mean, timestampdata.plan_optimal.states.speed, 3.0, self.dt
        )

        # Motion Profile Diagram
        # motion_future contains the current pos. hence 'index4pin2free' is  'i+1'
        self.p_ax234.update_profile(
            timestampdata.plan_optimal.states.velocity.mean,
            timestampdata.plan_optimal.states.speed,
            controls,
            index4pin2free=i + 1,
            magnitude_flag=magnitude_flag,
        )

        self.p_ax234.update_time_highlighter(self.dt * i)

    def update_others_cartesian(self, timestampdata, i):
        # print "timestamp: ", timestampdata.timestamp

        # iterate over all vehicles defined in Cartesian plot
        for v_id in list(self.p_ax1.vehicles.keys()):

            # ego vehicle is inside PlotCartesian vehicles; but it is updated in separate call.
            if v_id is self.vehicle_id:
                continue

            # if the vehicle is in current timestamp, use this data to set its position
            elif v_id in timestampdata.scene.scene_objects:
                v = timestampdata.scene.get_object(v_id)
                x, y = v.state.position.mean
                yaw = v.state.yaw.mean
                speed = v.state.speed
                uncertainty_ellipses = np.hstack(
                    [v.state.position.range(1)[3:], v.state.position.range(2)[3:], v.state.position.range(3)[3:]]
                )
                self.p_ax1.update_vehicle_plot(
                    v.id, x, y, yaw, speed, set_facecolor=True, uncertainty_ellipses=uncertainty_ellipses
                )

            elif v_id in timestampdata.environment.tracked_objects:
                v = timestampdata.environment.get_object(v_id)
                x, y = v.state.position.mean
                yaw = v.state.yaw.mean
                speed = v.state.speed
                uncertainty_ellipses = np.hstack(
                    [v.state.position.range(1)[3:], v.state.position.range(2)[3:], v.state.position.range(3)[3:]]
                )
                self.p_ax1.update_vehicle_plot(
                    v.id, x, y, yaw, speed, set_facecolor=False, uncertainty_ellipses=uncertainty_ellipses
                )

            # place the vehicle to nowhere
            else:
                self.p_ax1.update_vehicle_plot(v_id, 0.0, 0.0, 0.0, 0.0, uncertainty_ellipses=np.zeros(6))

    def update_others_frenet(self, timestampdata, i):
        self.p_ax0_pov.clear_objects()
        for v in timestampdata.situation.objects():
            c = timestampdata.scene.get_object(v.id).color
            for m in v.maneuvers.hypotheses:
                l_current = m.progress[0]
                self.p_ax0_pov.plot_object(m.motion, m.progress, m.overlap, c, offset=l_current)

    def update_timestamp_text(self, timestamp):
        assert isinstance(timestamp, int)
        self.timestamp_text.set_text("Timestamp = %6i" % timestamp)

    def __debug(self, timestampdata):
        self.ax1.plot(
            timestampdata.decision_base.corridor.center[:, 0],
            timestampdata.decision_base.corridor.center[:, 1],
            "-o",
            ms=4,
            color="red",
            lw=3,
        )
