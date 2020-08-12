from __future__ import division
from datetime import datetime


def get_settings(output_path):

    from mp_sim.configurations.settings import settings

    settings['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    settings['save_dir'] = str(output_path)  # will serve as save directory for figures

    # Number of timesteps (horizon is defined in seconds, not ms)
    N = int(settings['temporal']['horizon'] / (settings['temporal']['dt'] / 1000))
    settings['temporal']['N'] = N

    # Extract timestamps to be computed
    NN = int(settings['main']['travel_length']/ (settings['temporal']['dt'] / 1000))
    settings['main']['NN'] = NN

    return settings


def load_configurations(output_path, test_case_id):

    from mp_sim.configurations.test_cases import test_cases
    try:
        configurations = test_cases[test_case_id]
    except KeyError:
        raise Exception("The test case is not defined")

    s = get_settings(output_path)
    configurations.update(s)
    return configurations



"""
def replace_parameters(param_dict, param_spec, val):
    for i, p in enumerate(param_spec):

        param_terms = p.split('.')

        obj = param_dict
        for j in param_terms[:-1]:
            obj = obj[j]

        obj[param_terms[-1]] = val[i]


def test_runner(test_case_id, save_base):
    subdir_postfix_fmt = '__%s_%s'
    base_settings = deepcopy(sim_master.src.sim_master.settings.settings)
    test_case = test_cases[test_case_id]

    subdir = 'test_case_' + test_case_id + '__' + time.strftime('%H.%M.%S')

    save_dir = os.path.join(save_base, subdir)

    settings_override_global = test_case['settings_override_global']
    settings_override = test_case['settings_override_instance']

    print
    print 'Running test case <%s>.' % test_case_id
    print 'Description:'
    print test_case['desc']
    print 'Global parameters:'
    print settings_override_global
    print 'Varied parameters:'
    print settings_override
    print

    settings_global = deepcopy(base_settings)
    replace_parameters(settings_global, settings_override_global.keys(),
                       settings_override_global.values())

    if test_case['delete_map_data']:
        shutil.rmtree('MapData')

    if test_case['all_combinations']:
        param_vals = settings_override.values()
        param_vals = list(itertools.product(*param_vals))  # cartesian product

        param_keys = (settings_override.keys(), ) * len(param_vals)
    else:
        # sequential
        # param_vals = itertools.chain(*settings_override.values())
        # param_vals = [(i, ) for i in param_vals]
        #
        # param_keys = itertools.chain(*[((k, ), ) * len(v) for k, v in settings_override.iteritems()])

        # simultaneous
        param_vals = zip(*settings_override.values())
        param_keys = (settings_override.keys(), ) * len(param_vals)

    for param_key_tuple, param_val_tuple in zip(param_keys, param_vals):
        settings_instance = deepcopy(settings_global)
        replace_parameters(settings_instance, param_key_tuple, param_val_tuple)

        try:
            subdir_postfix = subdir_postfix_fmt % ('params', repr(param_val_tuple))
            main(save_base, instance_settings=settings_instance, subdir_postfix=subdir_postfix, subdir=subdir)
        except Exception as e:
            print traceback.format_exc()
            print 'Error occured for parameter combination <%s>' % repr(param_val_tuple)

            if not test_case['ignore_errors']:
                raise e

    # dump test case dict
    with open(save_dir + '/test_case_params.pck', 'w') as f:
        pickle.dump(test_case, f)

    # copy OSM file
    # TODO: what should be done if map param is varied?
    osm_name = settings_global['Map']['road_data'] + '.osm'
    osm_path = os.path.join(save_dir, 'osm_data')
    osm_new_path = os.path.join(osm_path, osm_name)

    os.makedirs(osm_path)

    shutil.copyfile('OSM_Data/'+osm_name, osm_new_path)

    # run post_exec script if specified
    if test_case['post_exec']:
        post_exec_path = test_case['post_exec'][0]
        post_exec_file = post_exec_path.split('/')[-1]
        post_exec_args = test_case['post_exec'][1:]

        # To support numeric args. pyplot bug, see: https://github.com/matplotlib/matplotlib/issues/1986
        post_exec_args = map(str, post_exec_args)

        # pass output directory if specified
        for i, v in enumerate(post_exec_args):
            if v == '$OUTPUT_DIR':
                post_exec_args[i] = save_dir

        post_exec_args = [post_exec_file] + post_exec_args

        print 'Running %s' % post_exec_file

        post_exec_module = __import__(post_exec_path, globals(), locals(), ['execute'])
        print dir(post_exec_module)
        post_exec_module.execute(*post_exec_args)
"""






