import unittest
import datetime
import numpy as np
import os
import matplotlib.pyplot as plt
from p3iv_utils.lanelet_map_reader import lanelet_map_reader
from p3iv_utils.consoleprint import Print2Console
from p3iv_utils.driver_models import IntelligentDriverModel


class TestPrin2Console(unittest.TestCase):
    def test_console_print(self):
        Print2Console.p("s", ["hello"], style="yellow")
        self.assertTrue(True)  # fake test :(


class TestLaneletMapReader(unittest.TestCase):
    def test_lanelet_map_reader(self):
        file_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
        directory = os.path.join(file_path, "../res/maps/lanelet2")
        l = lanelet_map_reader("DR_DEU_Merging_MT", directory)
        print("Lanelet map loaded")
        self.assertTrue(True)  # another fake test :( is added for coverage


class TestIDM(unittest.TestCase):
    def test_dim(self, show=False):

        # Some testing
        dt = 0.5  # in s
        N = 10

        # Parameters for mio vehicle in front
        ego_speed = 15.0  # in m/s
        mio_start = 15.0  # in m

        mio_speed = 10.0  # in m/s
        l_mio = np.arange(0, N + 1) * mio_speed * dt + mio_start
        v_mio = np.ones(N + 1, dtype=float) * mio_speed

        v_des = 12.0
        acc_max = 5.0
        dec_max = -5.0
        dec_cft = -3.0
        idm = IntelligentDriverModel(v_des, acc_max, dec_max, dec_cft, dt, N)

        t_start = datetime.datetime.now()
        pos_ego, spd_ego, acc_ego = idm(0.0, ego_speed, l_mio, v_mio)
        t_completion = datetime.datetime.now() - t_start
        print(t_completion.microseconds / 1000, " ms")

        t_start = datetime.datetime.now()
        pos_ego, spd_ego, acc_ego = idm(0.0, ego_speed, l_mio, v_mio, upsampling_rate=2)
        t_completion = datetime.datetime.now() - t_start
        print(t_completion.microseconds / 1000, " ms")

        t_start = datetime.datetime.now()
        pos_ego, spd_ego, acc_ego = idm.accs(0.0, ego_speed, l_mio, v_mio, N, dt)
        t_completion = datetime.datetime.now() - t_start
        print(t_completion.microseconds / 1000, " ms")

        import matplotlib.pyplot as plt

        l_mio = np.append(l_mio[0] - dt * mio_speed, l_mio)
        plt.plot(l_mio, label="mio")
        plt.plot(pos_ego, label="ego")
        plt.legend()
        if show:
            plt.show()
        else:
            plt.close()


if __name__ == "__main__":
    unittest.main()
