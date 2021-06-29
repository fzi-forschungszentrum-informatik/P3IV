from __future__ import division
import os
import yaml
from datetime import datetime


pkg_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.."))
pkg_path = os.path.realpath(pkg_path)


def read_yaml(filename):
    with open(filename, "r") as stream:
        try:
            d = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return d


def get_settings():

    fpath = os.path.join(pkg_path, "p3iv/configurations/settings.yaml")
    settings = read_yaml(fpath)

    settings["dataset"] = os.path.join(pkg_path, "../.", settings["dataset"])
    settings["start_time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # Number of timesteps (horizon is defined in seconds, not ms)
    N = int(settings["temporal"]["horizon"] / (settings["temporal"]["dt"] / 1000))
    settings["temporal"]["N"] = N

    return settings


def load_configurations(test_case_id):
    fpath = os.path.join(pkg_path, "p3iv/configurations/test_cases.yaml")
    test_cases = read_yaml(fpath)

    try:
        configurations = test_cases[test_case_id]
    except KeyError:
        msg = "The test case '" + test_case_id + "' is not found in p3iv/configurations/test_cases.py"
        raise KeyError(msg)

    s = get_settings()
    configurations.update(s)

    return configurations
