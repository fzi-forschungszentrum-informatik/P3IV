import numpy as np
from p3iv_visualization.cartesian.plot_cartesian import PlotCartesian
from p3iv_visualization.spatiotemporal.utils.plot_utils import PlotUtils
from p3iv_visualization.spatiotemporal.utils.plot_ego_motion import PlotEgoMotion
from p3iv_visualization.spatiotemporal.utils.plot_other_vehicles import PlotOtherVehicles
from util_motion.visualization.plot_motion_sequence import PlotMotionSequence
from animation_frame import AnimationFrame


class Animator(object):
    def __init__(self, lanelet_map_file, vehicle_id, vehicle_color, vehicles, dt, imagery_data=None, header=None):
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
            self.ax1, lanelet_map_file, center_vehicle_id=self.vehicle_id, imagery_data=imagery_data
        )
        self.p_ax1.fill_vehicles(vehicles)
        self.p_ax1.set_vehicle_plots()
        self.timestamp_text = self.ax1.text(0.65, 0.04, "", transform=self.ax1.transAxes, fontsize=8)

        self.p_ax234 = PlotMotionSequence(self.ax2, self.ax3, self.ax4)

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
        """
        timestampdata = v.timestamps.get(current_time)
        x, y = timestampdata.plan_optimal.motion.cartesian.position.mean[i_current]
        yaw = timestampdata.plan_optimal.motion.yaw_angle[i_current]
        self.p_ax1.update_vehicle_plot(v.v_id, x, y, yaw)
        """

        # The plots on ax0 are 'static'
        motion_profile = timestampdata.plan_optimal.motion

        # Path-time Diagram
        l_current = motion_profile.frenet.position.mean[-1, 0]
        l_current = 0.0

        # because l_current is subtrachted as offset, static axis limits can be attained
        self.p_ax0_pem.update_motion_profile(motion_profile, offset=l_current)
        # self.p_ax0_pem.update_stop_positions(motion_future, self.n_pin_future + 1)  # m. future contains the curr. pos
        # self.p_ax0_pem.update_initial_position(timestampdata.motion[-1])
        # self.p_ax0_pem.delete_motion_limits()
        # self.p_ax0_pem.plot_motion_limits(timestampdata.motion[-1])

        self.p_ax0_pu.set_axis_limits(-50.0, 100.0)
        self.p_ax0_pem.update_timelighter(i * self.dt)

        # Cartesian-Motion Diagram
        x, y = timestampdata.plan_optimal.motion.cartesian.position.mean[i]
        yaw = timestampdata.plan_optimal.motion.yaw_angle[i]
        visible_region = None  # timestampdata.environment.visible_areas

        self.p_ax1.update_vehicle_plot(
            self.vehicle_id,
            x,
            y,
            yaw,
            visible_region,
            zoom=self.frame.zoom,
            motion_past=motion_profile.cartesian.position.mean[: i + 1],
            motion_future=motion_profile.cartesian.position.mean[i:],
        )

        # Motion Profile Diagram
        # motion_future contains the current pos. hence 'index4pin2free' is  'i+1'
        self.p_ax234.update_profile(motion_profile.frenet, index4pin2free=i + 1, magnitude_flag=magnitude_flag)
        self.p_ax234.update_time_highlighter(self.dt * i)

    def update_others_cartesian(self, timestampdata, i):
        # print "timestamp: ", timestampdata.timestamp

        # iterate over all vehicles defined in Cartesian plot
        for v_id in self.p_ax1.vehicles.keys():

            # ego vehicle is inside PlotCartesian vehicles; but it is updated in separate call.
            if v_id is self.vehicle_id:
                continue

            # if the vehicle is in current timestamp, use this data to set its position
            elif v_id in timestampdata.scene.scene_objects:
                v = timestampdata.scene.get_object(v_id)
                """
                print "-------"
                print "v_id: ", v_id, v.color
                print v.current_lanelets

                if v_id == 62:
                    print timestampdata.timestamp
                    print v_id, v.color
                    print v.laneletsequences.new()
                    for l in v.laneletsequences:
                        print l.uuid
                        #print "..."
                    #print "----------"
                    #for sc in v.laneletsequence_scenes:
                    #    print sc.laneletsequence.uuid
                    print "----------"
                    for ul in v.laneletsequences.unique_directions():
                        print ul.centerline()
                """
                x, y = v.state.position.mean
                yaw = v.state.yaw.mean
                self.p_ax1.update_vehicle_plot(v.v_id, x, y, yaw, set_facecolor=True)

            elif v_id in timestampdata.environment.tracked_objects:
                v = timestampdata.environment.get_object(v_id)
                x, y = v.state.position.mean
                yaw = v.state.yaw.mean
                self.p_ax1.update_vehicle_plot(v.v_id, x, y, yaw, set_facecolor=False)

            # place the vehicle to nowhere
            else:
                self.p_ax1.update_vehicle_plot(v_id, 0.0, 0.0, 0.0)

    def update_others_frenet(self, timestampdata, i):
        self.p_ax0_pov.clear_objects()
        for v in timestampdata.situation.objects():
            c = timestampdata.scene.get_object(v.v_id).color
            for m in v.maneuvers.hypotheses:
                l_current = m.motion.frenet.position.mean[-1, 0]
                self.p_ax0_pov.plot_object(m.motion.frenet.position, c, offset=l_current)

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


if __name__ == "__main__":
    import sys
    import time
    import matplotlib.pyplot as plt
    from visualization.io.postprocessing_input import request_input2visualize

    directory = sys.argv[1]
    settings, vehicles, map_data, _, combination_id, current_time, _ = request_input2visualize(directory)

    dt = settings["Main"]["dt"]
    N = settings["Main"]["N"]
    N_pin_past = settings["Opt"]["ceres1d"]["N_pin_past"]
    N_pin_future = settings["Opt"]["ceres1d"]["N_pin_future"]
    map_image_name = settings["Map"]["road_data"]

    egovehicle = [v for v in vehicles if "ego" in v.vehicle_id][0]

    animator = Animator(
        map_image_name, map_data, egovehicle.vehicle_id, egovehicle.properties.color, vehicles, settings["Main"]["dt"]
    )

    animator.init_spatiotemporal_plot(N, N_pin_past, N_pin_future)
    animator.init_motion_profile(N, N_pin_past, N_pin_future)

    visible_region = vehicles[-1].timestampdata[current_time].environment.visible_regions
    vehicle_colors = vehicles[-1].timestampdata[current_time].decision_base.vehicle_colors
    combination = vehicles[-1].timestampdata[current_time].decision_base.combinations[combination_id]

    i = 10

    start = time.time()
    animator.update_ego(combination, vehicle_colors, visible_region, i=i)
    animator.update_others(vehicles[:-1], current_time, i=i)
    end = time.time()
    print "It took %f to update the plot" % (end - start)

    plt.show()
