# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import warnings
from p3iv_types.environment_model import EnvironmentModel
from p3iv_core.bindings.dataset import DataConverterInterface


class DataConverter(DataConverterInterface):
    def __init__(self, configurations):
        self._tracks = configurations["tracks"]  # note that this object is different than INTERACTION dataset tracks!

    def fill_environment(self, environment, *args):
        """Fill environment model with data from the dataset.

        Parameters
        ----------
        environment: EnvironmentModel
            Environmnet model object to be filled.
        """
        for v_id, tracks in list(self._tracks.items()):
            state = self.state(*tracks[1:-2])
            environment.add_object(v_id, self.get_color(v_id), tracks[-2], tracks[-1], state)
        return environment

    def get_state(self, timestamp, object_id):
        tracks = self._tracks[object_id]
        return self.state(*tracks[1:-2])
