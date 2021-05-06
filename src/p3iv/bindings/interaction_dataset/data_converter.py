from __future__ import division
import numpy as np
import warnings
from matplotlib import colors as mcolors
from external.dataset_types import Track
from p3iv.types.state import VehicleState
from util_motion.motion import Motion


def get_color(index):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    return colors.keys()[index]


class DatasetValueError(Exception):
    repr("Value not present in dataset")


class DataConverter(object):
    def __init__(self, dt, track_dictionary):
        assert isinstance(dt, int)
        assert isinstance(track_dictionary.values()[0], Track)

        self.dt = dt
        self.track_dictionary = track_dictionary

    def fill_environment(self, environment, timestamp):
        """Fill environment model with data from the dataset.

        Parameters
        ----------
        environment: EnvironmentModel
            Environmnet model object to be filled.
        timestamp: int
            Integer that of current timestamp.
        """
        assert isinstance(timestamp, int)

        for t_id, track in self.track_dictionary.items():
            motion = self.get_motion_with_current_timestamp(timestamp, t_id)
            if motion:
                environment.add_object(t_id, get_color(t_id), track.length, track.width, motion)
        return environment

    def get_state(self, timestamp, track_id):
        """Read from dataset in VehicleState-format. Extract only current timestamp state."""
        assert isinstance(track_id, int)
        assert isinstance(timestamp, int)

        if not track_id in self.track_dictionary:
            raise DatasetValueError

        track = self.track_dictionary[track_id]
        try:
            data = self._read_track_at_timestamp(track, timestamp)
            state = self._create_state_from_array(data)
        except DatasetValueError:
            state = None
            pass

        return state

    def get_motion_with_current_timestamp(self, timestamp, t_id):
        """Read from dataset in Motion-format. Ensure that the last value in timestamps is included."""
        assert isinstance(timestamp, int)
        assert isinstance(t_id, int)

        # timestamps until now
        timestamps = np.arange(100, int(timestamp) + 1, int(self.dt))

        try:
            timestamps_available, motion = self.get_motion(t_id, timestamps)
            if timestamps[-1] in timestamps_available:
                return motion
        except DatasetValueError:
            return None

    def get_motion(self, track_id, timestamps):
        """Read from dataset in Motion-format. Try to extract all timestamps provided."""
        assert isinstance(track_id, int)
        assert isinstance(timestamps, (list, np.ndarray))

        if not track_id in self.track_dictionary:
            raise DatasetValueError

        track = self.track_dictionary[track_id]
        data = np.empty([len(timestamps), 6])
        i_begin = 0
        i_available = 0
        for i, ts in enumerate(timestamps):
            try:
                data[i, :] = self._read_track_at_timestamp(track, ts)
                i_available += 1
            except DatasetValueError:
                if i == i_begin:
                    i_begin += 1
                pass

        i_end = i_begin + i_available

        if i_begin == len(timestamps):
            raise DatasetValueError

        data_available = data[i_begin:i_end, :]
        timestamps_available = timestamps[i_begin:i_end]
        motion = self._create_motion_from_array(data_available, self.dt / 1000.0)
        return timestamps_available, motion

    def read_track_at_timestamp(self, track_id, timestamp):
        if not track_id in self.track_dictionary:
            return None
        return self._read_track_at_timestamp(self.track_dictionary[track_id], timestamp)

    @staticmethod
    def _read_track_at_timestamp(track, timestamp):
        """Read track data at provided timestamp.
        Protected, as it serves as a helper func.
        """
        assert isinstance(timestamp, int)
        assert isinstance(track, Track)

        if not (track.time_stamp_ms_first <= timestamp <= track.time_stamp_ms_last):
            raise DatasetValueError

        data = np.empty(6)
        data[0] = timestamp
        data[1] = track.motion_states[timestamp].x
        data[2] = track.motion_states[timestamp].y
        data[3] = track.motion_states[timestamp].psi_rad
        data[4] = track.motion_states[timestamp].vx
        data[5] = track.motion_states[timestamp].vy
        return data

    @staticmethod
    def _create_motion_from_array(data_arr, dt):
        """Helper function to create Motion instance from motion-data-array."""
        motion = Motion()
        motion.resize(len(data_arr))
        motion.cartesian.position.mean[:, 0] = data_arr[:, 1]  # index 0 is timestamp
        motion.cartesian.position.mean[:, 1] = data_arr[:, 2]
        motion.yaw_angle = (np.degrees(data_arr[:, 3]) + 360.0) % 360.0
        motion.cartesian.velocity.mean[:, 0] = data_arr[:, 4]
        motion.cartesian.velocity.mean[:, 1] = data_arr[:, 5]
        return motion

    @staticmethod
    def _create_state_from_array(data_arr):
        """Helper function to create VehicleState instance from motion-data-array."""
        state = VehicleState()
        state.position.mean = data_arr[1:3]  # index 0 is timestamp
        state.yaw.mean = (np.degrees(data_arr[3]) + 360.0) % 360.0
        state.velocity.mean = data_arr[4:6]
        return state
