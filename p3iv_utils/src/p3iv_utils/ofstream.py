import time
import os
import simplejson as json


def create_output_dir():

    pkg_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    output_root_path = os.path.join(pkg_path, "../../p3iv/", "outputs")
    output_dir = os.path.normpath(output_root_path)

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    return output_dir


def create_output_path(output_dir_):

    save_dir_ = os.path.join(output_dir_, time.strftime("%Y-%m-%d/%H.%M.%S"))
    output_path = os.path.normpath(save_dir_)
    os.makedirs(output_path)
    return output_path


def save_settings(output_path, instance_settings):
    j_settings = json.dumps(instance_settings, indent=4)
    f_settings = open(output_path + "settings.json", "w")
    print(j_settings, file=f_settings)
    f_settings.close()
