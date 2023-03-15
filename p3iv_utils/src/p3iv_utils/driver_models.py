# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from scipy.interpolate import interp1d


class IntelligentDriverModel(object):
    def __init__(self, v_desired, acc_max, dec_max, dec_cft, dt, N):
        self._v_des = v_desired
        self._acc_max = acc_max  # maximum vehicle acceleration
        self._dec_max = -np.abs(dec_max)
        self._dec_cft = -np.abs(dec_cft)  # comfortable braking deceleration
        self._dt = dt
        self._N = N

        self._H_DES = 1.0  # desired time-headway
        self._D_SAFETY = 2.0  # safe distance
        self._L_VEHICLE = 3.0  # vehicle length

    def __call__(self, l_ego, v_ego, l_front_array, v_front_array, upsampling_rate=1.0, v_des=None):
        if v_des is not None:
            self._v_des = v_des

        # v_front_array = np.diff(l_front_array)
        # v_front_array = np.append(v_front_array, v_front_array[-1])

        if int(upsampling_rate) == 1.0:
            return self.accs(l_ego, v_ego, l_front_array, v_front_array, self._N, self._dt)
        else:
            return self.upsampled_accs(l_ego, v_ego, l_front_array, v_front_array, upsampling_rate=upsampling_rate)

    def acc(self, l_ego, v_ego, l_front, v_front):

        # net distance = front_vehicle_position - ego_vehicle_position - ego_vehicle_length
        d = l_front - l_ego - self._L_VEHICLE  # V2C-distance
        s_star = self._s_star(v_ego, v_front)

        interaction_term = (s_star / d) ** 2
        acceleration_term = (v_ego / self._v_des) ** 4

        acceleration_term = np.clip(acceleration_term, 0, 2)  # TODO: hand-crafted intervals. no idea if valid!
        interaction_term = np.clip(interaction_term, 0, 2)
        deceleration_term = acceleration_term + interaction_term

        beta = 1 - deceleration_term

        if beta < 0.0:
            # the vehicle will brake
            idm_acc = np.clip(np.abs(beta), 0, 1) * self._dec_max
        else:
            idm_acc = np.clip(np.abs(beta), 0, 1) * self._acc_max

        return idm_acc

    def accs(self, l_ego, v_ego, l_front_array, v_front_array, N, dt):
        """
        Calculate accelerations. The resulting array includes current values!
        Prefer upsampled one if you are using dt~=100ms.
        """
        idm_pos_array = np.empty(N + 1)
        idm_spd_array = np.empty(N + 1)
        idm_acc_array = np.empty(N + 1)
        idm_pos_array[0] = l_ego
        idm_spd_array[0] = v_ego
        idm_acc_array[0] = 0.0

        l_front_array = self._equalize_lengths(l_front_array, N + 1)
        v_front_array = self._equalize_lengths(v_front_array, N + 1)

        for i in range(1, N + 1):

            idm_acc = self.acc(l_ego, v_ego, l_front_array[i], v_front_array[i])

            v_ego = v_ego + idm_acc * dt
            if v_ego < 0:
                v_ego = 0
                if idm_acc < v_ego / dt:
                    idm_acc = v_ego / dt

            displacement = v_ego * dt + 0.5 * idm_acc * (dt**2)
            l_ego = l_ego + displacement

            idm_pos_array[i] = l_ego
            idm_spd_array[i] = v_ego
            idm_acc_array[i] = idm_acc

        return idm_pos_array, idm_spd_array, idm_acc_array

    def upsampled_accs(self, l_ego, v_ego, l_front_array, v_front_array, upsampling_rate=4.0):

        h = self._dt / upsampling_rate
        N_upsampled = int(self._N * upsampling_rate)

        sampled_times = list(range(0, self._N + 1))
        upsampled_times = np.linspace(0, self._N, N_upsampled + 1)

        l_front_array = self._equalize_lengths(l_front_array, self._N + 1)
        v_front_array = self._equalize_lengths(v_front_array, self._N + 1)

        f_pos_upsample = interp1d(sampled_times, l_front_array)
        l_front_array = f_pos_upsample(upsampled_times)
        f_spd_upsample = interp1d(sampled_times, v_front_array)
        v_front_array = f_spd_upsample(upsampled_times)

        p, v, a = self.accs(l_ego, v_ego, l_front_array, v_front_array, N_upsampled, h)

        idm_pos_downsampled = p[:: int(upsampling_rate)]
        idm_spd_downsampled = v[:: int(upsampling_rate)]
        idm_acc_downsampled = a[:: int(upsampling_rate)]

        return idm_pos_downsampled, idm_spd_downsampled, idm_acc_downsampled

    @staticmethod
    def _any_object_in_front(l_front, v_front):
        if (l_front == 0.0) and (v_front == 0.0):
            return True
        else:
            return False

    def _s_star(self, v_ego, v_front):
        d_min = self._H_DES * v_ego  # desired  min. time-distance
        s_star = (
            self._D_SAFETY + d_min + (v_ego * (v_ego - v_front) / (2 * np.sqrt(np.abs(self._acc_max * self._dec_cft))))
        )
        return s_star

    @staticmethod
    def _equalize_lengths(input_array, ref_length):
        if ref_length - len(input_array) == 1:
            return np.append(input_array[0], input_array)
        elif len(input_array) == ref_length:
            return input_array
        else:
            raise Exception("Sizes do not match!")
