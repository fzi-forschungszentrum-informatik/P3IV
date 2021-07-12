# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from __future__ import division
import numpy as np
import warnings
import random
import matplotlib.pyplot as plt
from .external.dataset_types import Track
from p3iv_types.motion import MotionState


colormap = plt.cm.get_cmap("jet", 20)


class DatasetValueError(Exception):
    repr("Value not present in dataset")


class DataConverter(object):
    def __init__(self, dt, track_dictionary):
        assert isinstance(dt, int)
        assert isinstance(list(track_dictionary.values())[0], Track)

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

        for t_id, track in list(self.track_dictionary.items()):
            state = self.get_state(timestamp, t_id)
            if state:
                environment.add_object(t_id, colormap(t_id % 20), track.length, track.width, state)
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

    def read_track_at_timestamp(self, track_id, timestamp):
        if not track_id in self.track_dictionary:
            return None
        return self._read_track_at_timestamp(self.track_dictionary[track_id], timestamp)

    @staticmethod
    def _read_track_at_timestamp(track, timestamp):
        """Read track data at provided timestamp.
        Protected, as it serves as a helper func.
        """
        assert isinstance(timestamp, (int, np.int, np.int64))
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
    def _create_state_from_array(data_arr):
        """Helper function to create MotionState instance from motion-data-array."""
        state = MotionState()
        state.position.mean = data_arr[1:3]  # index 0 is timestamp
        state.yaw.mean = (np.degrees(data_arr[3]) + 360.0) % 360.0
        state.velocity.mean = data_arr[4:6]
        return state
