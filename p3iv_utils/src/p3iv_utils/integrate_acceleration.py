
import numpy as np
from scipy.interpolate import interp1d


def generate_position_velocity_acc_array(
    action_sequence, s_0, v_0, n_sim_timesteps, n_pin_future=0, dt_sim=0.1, dt_motion=0.5
):
    """
    Integrates the acceleration profile 2 times
    append n_pin_future points at the end
    n_sim_timesteps = N (from configurations)
    """
    assert dt_motion >= dt_sim
    # assert (dt_motion % dt_sim == 0)

    horizon = n_sim_timesteps * dt_sim
    n_actions = len(action_sequence)
    assert (n_actions - 1) * dt_motion == n_sim_timesteps * dt_sim

    # generate acceleration step profile for horizon
    h_motion = np.arange(0, (n_actions) * dt_motion, dt_motion)
    acc_func = interp1d(h_motion, action_sequence, kind="zero")

    t_sim = np.arange(0, horizon, dt_sim)
    acc = acc_func(t_sim)

    # TODO append n_pin_future points

    x = np.zeros((3, n_sim_timesteps + 1))
    x[:, 0] = np.array([s_0, v_0, 0])

    half_dt_sim_square = 0.5 * dt_sim ** 2

    for i in range(n_sim_timesteps):
        x[0, i + 1] = x[0, i] + dt_sim * x[1, i] + half_dt_sim_square * acc[i]
        x[1, i + 1] = x[1, i] + dt_sim * acc[i]
        x[2, i + 1] = acc[i]

    return x[:, 1:]
