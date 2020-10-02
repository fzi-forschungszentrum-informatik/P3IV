from util_simulation.vehicle.main import Vehicle
from mp_sim.modules import VehicleModules
from understanding.lanelet_sequence_analyzer import LaneletSequenceAnalyzer
from interpolated_distance.coordinate_transformation import CoordinateTransform


def use_interaction_sim_data(instance_settings):

    from interaction_prediction_sim.interaction_data_extractor import track_reader
    from interaction_prediction_sim.interaction_data_handler import InteractionDataHandler

    track_dictionary = track_reader(instance_settings["map"])
    data_handler = InteractionDataHandler(int(instance_settings["temporal"]["dt"]*1000), track_dictionary)
    object_list = data_handler.fill_situation(instance_settings["timestamp_begin"])

    return object_list


def create_simulation_objects(object_list, laneletmap, configurations):

    ground_truth_objects = []
    lanelet_sequence_analyzer = LaneletSequenceAnalyzer(laneletmap)

    for o in object_list:
        v = Vehicle(o.v_id)
        v.appearance.color = o.color
        v.appearance.length = o.length
        v.appearance.width = o.width

        # v.objective.route = ""
        # v.objective.set_speed = ""

        if o.v_id != configurations['vehicle_of_interest']:
            v.perception.sensor_fov = configurations['perception']['otherVehicle_sensor_fov']
            v.perception.sensor_range = configurations['perception']['otherVehicle_sensor_range']
        else:
            v.perception.sensor_fov = configurations['perception']['egoVehicle_sensor_fov']
            v.perception.sensor_range = configurations['perception']['egoVehicle_sensor_range']
        v.perception.sensor_noise = configurations['perception']['perception_noise']

        v.modules = VehicleModules(configurations, laneletmap, v)

        # extract frenet motion
        lanelet_path_wrapper = lanelet_sequence_analyzer.match(o.motion)
        centerline = lanelet_path_wrapper.centerline()
        c = CoordinateTransform(centerline)
        pos_frenet = c.xy2ld(o.motion.cartesian.position.mean)
        o.motion.frenet(pos_frenet, dt=0.1)

        # fill tracked motion
        v.timestamps.create_and_add(configurations['timestamp_begin'])
        v.timestamps.latest().motion = o.motion

        # fill initial values of KF
        v.modules.localization.setup_localization(pos_frenet[-1, 0], o.speed, 0.0)

        if o.v_id != configurations['vehicle_of_interest']:
            ground_truth_objects.append(v)
        else:
            voi = v
    ground_truth_objects.append(voi)

    return ground_truth_objects
