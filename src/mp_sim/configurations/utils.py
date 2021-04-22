from __future__ import division
from datetime import datetime


def get_settings():

    from mp_sim.configurations.settings import settings

    settings['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # Number of timesteps (horizon is defined in seconds, not ms)
    N = int(settings['temporal']['horizon'] /
            (settings['temporal']['dt'] / 1000))
    settings['temporal']['N'] = N

    return settings


def load_configurations(test_case_id):

    from mp_sim.configurations.test_cases import test_cases
    try:
        configurations = test_cases[test_case_id]
    except KeyError:
        msg = "The test case '" + test_case_id + \
            "' is not found in src/configurations/test_cases.py"
        raise Exception(msg)

    s = get_settings()
    configurations.update(s)

    return configurations
