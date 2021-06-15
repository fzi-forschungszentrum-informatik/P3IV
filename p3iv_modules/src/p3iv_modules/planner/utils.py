
import numpy as np
from scipy.interpolate import interp1d
from p3iv_utils.coordinate_transformation import CoordinateTransform
from p3iv_types.motion_plans import MotionPlan, MotionPlans


def get_MotionPlan_from_1D(centerline, cartesian_positions, frenet_l_array, dt, *args, **kwargs):
    """
    Given a longitudinal Frenet array with Frenet-frame starting from current position projected onto centerline,
    calculate both 2D-Frenet and 2D-Cartesian arrays.
    """

    ld_array = np.zeros([len(frenet_l_array), 2])
    ld_array[:, 0] = frenet_l_array

    xy_s, ld_array = convert_Frenet2Cartesian(centerline, cartesian_positions, ld_array)

    mp = MotionPlan()
    mp.motion(xy_s, dt=dt)
    return mp


def get_MotionPlan_from_2D(centerline, cartesian_positions, frenet_ld, dt, *args, **kwargs):

    mp = MotionPlan()
    mp.motion.cartesian(cartesian_positions, dt=dt)

    c = CoordinateTransform(centerline)
    frenet_positions = c.xy2ld(cartesian_positions)
    offset = frenet_positions[0, 0] - frenet_ld[0]
    frenet_positions[:, 0] = frenet_positions[:, 0] - offset
    mp.motion.frenet(frenet_positions, dt=dt)
    return mp


def convert_Frenet2Cartesian(corridor_center, cartesian_position, ld_array):
    """
    Given a corridor-center reference, past four Cartesian coordinates and a 2D-Frenet array including past four driven
    values, converts the Frenet-coordinate array to Cartesian coordinates and returns this.
    """

    c = CoordinateTransform(corridor_center)

    initial_l, initial_d = c.xy2ld(cartesian_position)
    ld_array[0, 1] = initial_d
    # 'initial_d' can be set equal to all columns. However, this will lead to
    # Frenet lon-coordinate matching to a value different than the one here

    # Correct offset errors resulting from selection of different arcs and/or transformation errors.
    # (Frenet coordinates in simulation env. are calculated using Lanelet2.
    # Here we use Interp. Distance, which is more precise. In some cases there is a tiny < 0.1m offset
    # between these. In cont. closed-loop simulation this error may accumulate and ruin the results.)
    # (The last Cartesian corresponds to 4th point, therefore the index 3)
    offset_l = ld_array[0, 0] - initial_l

    # convert only planned points
    ld_future_array = np.empty([len(ld_array) - 1, 2])
    ld_future_array[:, 0] = ld_array[1:, 0] - offset_l
    ld_future_array[:, 1] = ld_array[1:, 1]

    xy_future = c.ld2xy(ld_future_array)
    xy_s = np.vstack([cartesian_position, xy_future])

    return xy_s, ld_array


def match_sampling_intervals(solver_position_array, dt_simulation=0.1, dt_solver=0.5):
    """Perform interpolation if solver sampling interval is bigger than those of simulation.
    Returns upsampled (position) array.
    """
    assert dt_solver >= dt_simulation
    assert dt_solver % dt_simulation == 0

    r = int(dt_solver / dt_simulation)

    n_interpolated = int(len(solver_position_array) * r)

    f = interp1d(list(range(0, len(solver_position_array) + 1)), solver_position_array)
    simulation_position_array = f(n_interpolated)

    return simulation_position_array
