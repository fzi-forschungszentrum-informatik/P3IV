import numpy as np


class PlotEgoMotion(object):
    def __init__(self, ax, vehicle_id, vehicle_color):
        self.ax = ax
        self.id = vehicle_id
        self.color = vehicle_color

        self.time_range = None

        self.lines_line2d_motion_profile = None
        self.lines_line2d_motion_desired = None
        self.lines_line2d_stop_points = None
        self.lines_line2d_initial_pos = None
        self.lines_axvline = None
        self.coll_poly_unreach_upper = None
        self.coll_poly_unreach_lower = None

    def create_motion_profile(self, dt, N, linewidth=5, ms=3.0):
        self.time_range = dt * np.arange(N + 1)
        (self.lines_line2d_motion_profile,) = self.ax.plot([], [], "o-", linewidth=linewidth, color=self.color, ms=ms)

    def update_motion_profile(self, motion_profile, offset=0.0):
        assert len(self.time_range) == len(motion_profile)
        self.lines_line2d_motion_profile.set_data(self.time_range, motion_profile.frenet.position.mean[:, 0] - offset)

    def plot_motion_limits(self, motion_executed):

        # get upper motion limit
        u = motion_executed.safety.acceler_traj[-len(self.time_range) :]
        # '[-len(self.time_range):]' --> the acceler_traj contains values for the past points as well

        # get lower motion limit
        l = motion_executed.safety.braking_traj[-len(self.time_range) :]

        # dummy value
        z = 1000.0

        self.coll_poly_unreach_upper = self.ax.fill_between(self.time_range, u + z, u, facecolor=self.color, alpha=0.1)
        self.coll_poly_unreach_lower = self.ax.fill_between(self.time_range, l, l - z, facecolor=self.color, alpha=0.1)

    def delete_motion_limits(self):
        # todo: find a better way to set data
        try:
            self.coll_poly_unreach_upper.remove()
            self.coll_poly_unreach_lower.remove()
        except AttributeError:
            # if (coll_poly_unreach)s do not exits, it will raise an AttributeError
            pass

    def create_desired_motion(self):
        (self.lines_line2d_motion_desired,) = self.ax.plot([], [], color="r", linestyle="--", alpha=0.8, linewidth=1)

    def update_desired_motion(self, l_start, speed_desired):
        desired_motion_l = [l + l_start for l in self.time_range * speed_desired]
        self.lines_line2d_motion_desired.set_data(self.time_range, desired_motion_l)

    def create_stop_positions(self):
        (self.lines_line2d_stop_points,) = self.ax.plot([], [], "+", ms=6, color=self.color)

    def update_stop_positions(self, motion_planned, n_pts):
        t = self.time_range[:n_pts]
        l = motion_planned.safety.stop_positions[:n_pts]
        assert len(t) == len(l)
        self.lines_line2d_stop_points.set_data(t, l)

    def create_braking_motions(self):
        # for traj in comb_obj.safety.braking_traj:
        #    ax.plot(np.arange(1, N+1)*dt, traj, 'o-', linewidth=0.1, color="blue", alpha=0.4, ms=1)
        pass

    def update_braking_motions(self):
        pass

    def create_initial_position(self):
        (self.lines_line2d_initial_pos,) = self.ax.plot([], [], "*", ms=10, color=self.color)

    def update_initial_position(self, motion_profile_current):
        l_start = motion_profile_current.frenet.position.mean[0]
        self.lines_line2d_initial_pos.set_data(0, l_start)

    def create_time_highlighter(self):
        self.lines_axvline = self.ax.axvline(x=-1, linewidth=0.5, color="r")

    def update_timelighter(self, x):
        self.lines_axvline.set_xdata(x)
