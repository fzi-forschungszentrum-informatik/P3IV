import pickle
from p3iv.types.vehicle import Vehicle


class GroundTruth(dict):
    def __init__(self):
        super(GroundTruth, self).__init__()

    def append(self, vehicle):
        assert isinstance(vehicle, Vehicle)
        assert vehicle.v_id not in self.keys()
        self[vehicle.v_id] = vehicle

    def update(self, vehicle):
        assert isinstance(vehicle, Vehicle)
        assert vehicle.v_id in self.keys()
        self[vehicle.v_id] = vehicle

    def vehicles(self):
        return self.values()

    def get_vehicle(self, vehicle_id):
        assert vehicle_id in self.keys()
        return self[vehicle_id]

    def dump(self, pickle_filename):
        for v in self.vehicles():
            delattr(v, "modules")
        outfile = open(pickle_filename, "wb")
        pickle.dump(self, outfile)
        outfile.close()
