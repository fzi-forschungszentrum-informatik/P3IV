from __future__ import division
from visualization.spatiotemporal.utils.plot_utils import PlotUtils
from visualization.spatiotemporal.utils.plot_other_vehicles import PlotOtherVehicles


def plot_prediction(situation_model_objects, host_vehicle_id, N, dt, save_dir):

    for situation_object_id, situation_object in situation_model_objects.iteritems():
        for mh in situation_object.maneuver_hypotheses.get_maneuvers():
            header = (
                host_vehicle_id + "_predicts_" + situation_object.vehicle_id + "_with_intention_" + mh.intention_class
            )

            p = PlotUtils()
            p.create_figure(header)
            p.set_settings(dt, N, save_dir)

            pov = PlotOtherVehicles(p.ax, p.dt)
            weight = mh.probability.total
            pov.plot_object(mh.uncertain_motion, situation_object.vehicle_color, weight=weight)

            p.save_figure()
