import numpy as np
import warnings
from p3iv_utils.consoleprint import Print2Console


class ValueIntervalChecker(object):
    def __init__(self, value_name, max_val, min_val):
        self.value_name = value_name
        self.max_val = max_val
        self.min_val = min_val

    def check_value(self, value):
        if not (self.max_val >= value >= self.min_val):
            # warnings.warn(self.value_name + " value (" + str(value) + ") invalid!")
            string = self.value_name + " value (" + str(value) + ") invalid!"
            Print2Console.p("s", [string], style="red")

    def reset_bounds(self, max_val, min_val):
        self.max_val = max_val
        self.min_val = min_val


class PlannerDebugger(object):
    def __init__(self, configs, max_speed, max_acceleration, max_deceleration):
        self.n = None
        self._n_pin_past = configs["N_pin_past"]
        self._n_pin_future = configs["N_pin_future"]
        self._dt = configs["dt"] / 1000
        self._max_deceleration = max_deceleration

        self._brk_val_checker = ValueIntervalChecker("Stop position", 1e8, 0.0)
        self._spd_val_checker = ValueIntervalChecker("Speed", max_speed, 0.0)
        self._acc_val_checker = ValueIntervalChecker(
            "Acceleration", max_acceleration, self._max_deceleration
        )  # todo@Sahin: replace

        self._bound_upper = None
        self._bound_lower = None

        self._motion_planned = None

    def set_profile(self, motion_planned):
        self.n = len(motion_planned)
        self._motion_planned = motion_planned
        self._check_bound_length(self.n)

    def set_bounds(self, bound_upper, bound_lower):
        assert len(bound_upper) == len(bound_lower)
        self._bound_upper = bound_upper
        self._bound_lower = bound_lower

    def _check_bound_length(self, len_frenet_coords):
        k = self._n_pin_past - 1
        if len_frenet_coords - len(self._bound_lower) == k:
            self._bound_upper = np.append([self._bound_upper[0]] * k, self._bound_upper)
            self._bound_lower = np.append([self._bound_lower[0]] * k, self._bound_lower)

        if len(self._bound_upper) - len_frenet_coords == 1:
            self._bound_upper = self._bound_upper[1:]
            self._bound_lower = self._bound_lower[1:]

        assert len(self._bound_lower) == len_frenet_coords

    def print_frenet_bounds(self):
        print("\n")
        Print2Console.p("sf", ["l-coord. of initial pos.", self._motion_planned.frenet.position[self._n_pin_past, 0]])
        Print2Console.p("ssss", ["i", "lower", "pos", "upper"], style="underline")
        for i in range(self.n):
            if i is not self._n_pin_past - 1:
                Print2Console.p(
                    "sfff",
                    [str(i), self._bound_lower[i], self._motion_planned.frenet.position[i, 0], self._bound_upper[i]],
                )
            else:
                Print2Console.p(
                    "sfff",
                    [
                        str(i) + " (t=0)",
                        self._bound_lower[i],
                        self._motion_planned.frenet.position[i, 0],
                        self._bound_upper[i],
                    ],
                    style="bright",
                )
        print("\n")

    def print_stop_position_bounds(self):
        print("\n")
        Print2Console.p("ssss", ["i", "lower", "stop pos", "upper"], style="underline")
        for i in range(2 * self._n_pin_future + self._n_pin_past):
            # i+4: the braking calculations do not include values for the current position
            Print2Console.p(
                "sfff",
                [str(i), self._bound_lower[i], self._motion_planned.safety.stop_positions[i], self._bound_upper[i]],
            )

            self._brk_val_checker.reset_bounds(self._bound_upper[i], self._bound_lower[i])
            self._brk_val_checker.check_value(self._motion_planned.safety.stop_positions[i])
        print("\n")

    def print_motion_details(self, solution=False):
        print("\n")
        Print2Console.p("ssss", ["i", "speed", "acceleration", "jerk"], style="underline")
        for i in range(self.n):

            self._spd_val_checker.check_value(self._motion_planned.frenet.velocity[i, 0])
            self._acc_val_checker.check_value(self._motion_planned.frenet.acceleration[i, 0])

            if i is not self._n_pin_past - 1:
                Print2Console.p(
                    "ifff",
                    [
                        i,
                        self._motion_planned.frenet.velocity[i, 0],
                        self._motion_planned.frenet.acceleration[i, 0],
                        self._motion_planned.frenet.jerk[i, 0],
                    ],
                )
                if self._motion_planned.frenet.velocity[i, 0] < 1.0 and solution and i > self._n_pin_past:
                    input("Speed probably unsuitable!")
            else:
                Print2Console.p(
                    "sfff",
                    [
                        str(i) + " (t=0)",
                        self._motion_planned.frenet.velocity[i, 0],
                        self._motion_planned.frenet.acceleration[i, 0],
                        self._motion_planned.frenet.jerk[i, 0],
                    ],
                    style="bright",
                )
        print("\n")

    def all(self, profile_type, solution=False):
        assert type(profile_type) == str
        Print2Console.p("s", [profile_type], style="magenta", bold=True)
        self.print_motion_details(solution=solution)
        self.print_frenet_bounds()
        self.print_stop_position_bounds()
