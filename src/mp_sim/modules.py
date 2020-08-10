from perception.main import Percept
from localization.main import Localization
from understanding.main import Understand
from prediction.main import Predict
from decision_making.main import Decide
from lightsaber_interface.planner_interface import PlannerInterfacePyWrapper
from action.main import Act


class VehicleModules(object):
    def __init__(self, configurations, laneletmap, vehicle):

        self.localization = Localization(configurations["temporal"]["dt"], measurement_noise=configurations["localization"]["measurement_noise"],
                                         process_noise=configurations["localization"]["process_noise"])

        self.perception = Percept(laneletmap, vehicle.perception.sensor_fov, vehicle.perception.sensor_fov,
                                  vehicle.perception.sensor_noise, override_visibility=configurations['perception']['override_visibility'])

        """
        self.understanding = Understand(self.properties.route,
                            self.settings["Main"]["provably_safe_planning"],
                            self.settings["Main"]["dt"],
                            self.timestamps,
                            self.timestampdata)
       """
        self.prediction = Predict(configurations["temporal"]["dt"], configurations["temporal"]["N"], laneletmap)

        """
        Decide.__init__(self,
                        self.properties.max_acceleration,
                        self.properties.max_deceleration,
                        self.properties.set_speed,
                        self.settings["Main"]["dt"],
                        self.settings["Main"]["N"],
                        self.settings["Opt"]["ceres1d"]["N_pin_future"],
                        self.settings["Opt"]["initialization_astar"])

        Plan.__init__(self,
                      self.settings["Opt"])

        Act.__init__(self)
        """
