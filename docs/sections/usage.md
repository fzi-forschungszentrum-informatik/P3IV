## Execution


The simulation framework can be executed as
```shell
cd p3iv/p3iv/scripts
python main.py --run=DEU_Roundabout_OL_01
```
This command executes the test case `DEU_Roundabout_OL_01` defined inside `p3iv/src/p3iv/configurations/test_cases.py`. After each simulation run, the outputs are stored inside `p3iv/p3iv` with their directory names reflecting the start time of the simulation run.

If you have any problems and need help, you can execute
```shell
python main.py --help
```
for additional information. If this doesn't help, please refer to [FAQ](##FAQ).

## Visualization & Postprocessing

If you want to display inspect the results of a simulation, you can either execute
```shell
python main.py --show-single=<TIMESTAMP_VALUE>
```
or
```shell
python main.py --show-multi
```
These commands will start animations on the outcomes of planned trajectories. The first command will animate the planning results for a single timestamp ``<TIMESTAMP_VALUE>`` by iterating over individual timesteps, whereas the latter will iterate over all the timestamps at which planning is performed and will animate these.

## Configurations

In P3IV there two types of configurations that a user can modify:
- test cases
- simulation settings

Test cases are located inside `p3iv/p3iv_core/src/p3iv_core/configurations/test_cases.py`. This file contains a dictionary with key representing names that can be used an argument for the main script, e.g. `python main.py --run=<TEST_CASE_KEY>`. Every test case specifies the begin and end timestamps of the simulation, the ID of the ego (or host) vehicle. With the key `planning_meta`, it specifies as a dictionary with keys representing the IDs of the vehicle where the vehicle is heading to and with values both the lanelet ID where that heading to and the type of planner the vehicle with that ID is heading to. All vehicle IDs defined in `planning_meta` do closed-loop simulation. In other words, they react to the changes in the simulation environment.

The simulation settings are located inside `p3iv/p3iv_core/src/p3iv_core/configurations/settings.py`. This files defines parameters such as planning horizon, location of a drone dataset, levels of uncertainty. Therefore, whereas the former one, `test_cases.py` describe the test scene, this describes the individual parameters of the test scenario.

Independent of the defined configurations in these two files, every module written by the users can contain other configuration files. This is up to the user. The users can also modify and extend these settings to match their needs.

## Customization

Researchers frequently have to adapt the simulation settings to match the needs of their application. Even though, the framework has a clean layout, it may still be confusing for inexperienced researchers in python, catkin, or cmake.

### Catkin package structure

The simulation framework is aimed to have a modular structure and to work with flexibly with various ROS packages and modules. Catkin package layout and CMake meets this requirement perfectly.

The structure of a catkin package layout as illustrated below.

```
.
├── CMakeLists.txt
├── include
│   └── example_pkg
│       ├── internal
│       │   └── header_file.hpp
│       ├── header_a.hpp
│       └── header_b.hpp
├── LICENSE
├── package.xml
├── python_api
│   ├── py_example_pkg.cpp
│   └── py_example_pkg.hpp
├── README.md
├── res
│   └── resource.txt
├── setup.py
├── src
│   └── example_pkg
│       ├── converters
│       │   ├── __init__.py
│       │   └── a2b.py
│       ├── __init__.py
│       ├── parser.py
│       └── visualization
│           ├── __init__.py
│           └── plot_utils.py
└── test
    ├── test_file_cpp_impl.cpp
    └── test_file_py_impl.py
```
In a catkin package any python module or subpackage is located below ``<PACKAGE_NAME>/src/<PACKAGE_NAME>``. After building, a sourced environment can be import modules with ``from <PACKAGE_NAME> import <MODULE_NAME>``.

.. seealso::
   `ROS wiki <https://wiki.ros.org/catkin>`__ on catkin.

### Test files and scripts

Packages have test cases for coverage and CI testing. These tests are located inside `<PACKAGE_NAME>/test/` directory. Likewise, packages serving as tool have python scripts located inside ``scripts``. These are implemented for execution.

.. tip::
   Even though tests are implemented for testing, they can serve as examples.


### Layout
The `p3iv` itself is shipped as a catkin metapackage, e.g. a package that contains multiple other packages. It contains:
```
.
├── p3iv
├── p3iv_core
├── p3iv_modules
├── p3iv_types
├── p3iv_utils
├── p3iv_utils_polyline
├── p3iv_utils_polyvision
├── p3iv_utils_probability
└── p3iv_visualization
```
The package `p3iv/p3iv` is the metapackage that is "binding" other packages. As introduces above, it contains the scripts to execute the simulation environment and serves as directory to store simulation results.

The core functions to run the environment are inside `p3iv/p3iv_core`. Bindings to data sources such as drone datasets, functions to run the simulation framework and configuration files are located in this package.

The simulation framework instantiates a vehicle with perception, understanding, decision making, planning and action (or control) modules. For these different modules or later on by user custom added modules to work with each other, either common types and interfaces, or messages must be predefined. Indicated in the Section  [_"What P3IV is not?"_](##What-is-P3IV-not?) we do not define messages with timestamps. But for modules to operate with each other, we define interfaces as abstract classes and data types.

The default (or _exemplary_) modules together with their interface definitions are located inside `p3iv/p3iv_modules`:
```
.
├── action
├── decision
├── interfaces
├── perception
├── planner
├── prediction
└── understanding
```
The subdirectory `interfaces` contain abstract classes that define the interfaces these modules must match. These interfaces ensure the simulation environment to work with appropriate module definitions, preventing any incompatibility.

A vehicle instantiates these modules from the class `VehicleModules` in `p3iv/p3iv_modules/src/p3iv_modules/modules.py`. During instantiation, it checks whether instantiated modules follow the interfaces. During execution, it calls these module for every timestamp. These modules calculate the required output, such as predicted motion of other vehicles around for every *timestep* in the planning horizon. A user is free to modify and extend these data types and interfaces.

The data types serve both as baseline and as a guideline for future improvements. These are located inside `p3iv/p3iv_types`. Note that, this package has also type implementations for C++ and their PyBind bindings for Python-use.

While developing algorithms, researchers frequently need some common functions. Most of the time, such functions are implemented in various libraries. However, some application specific utilities are sometimes hard to fine. `p3iv/p3iv_utils` contains a small amount of useful functions. P3IV is shipped with useful utility functions, that can be used independently. Name of such packages start with ``p3iv_utils_`` prefix. Utility functions are described in next section in detail.

Visualization can guide researchers for possible improvements and help with debugging. Because there isn't a single visualization that depicts all possible metrics, visualization is implement in an object-oritented fashion but in a very modular way. Every visualization function is a class, that can accept instances of others, e.g. Cartesian plot instantiates the class that depicts vehicles and the class that depict a Lanelet2 map. Such functions are located inside `p3iv/p3iv_visualization`.


.. note::
   Note that some modules may have modified ``__init__.py`` files, as in the case of ``p3iv/p3iv_modules/src/p3iv_modules/interfaces/``.


### Data processing structure of the framework

The simulation framework runs staring from `timestamp_begin` defined in `test_cases.py` and finishes at `timestamp_end` defined in the same file. It sequentially executes the modules and returns the output. If the `simulation_type` is closed-loop, it updates its current position based on the planned value. An open-loop usage requires presence of a dataset, as it reads data from such a source to update for the next timestamp.

Upon execution, the simulation framework starts sequentially executing the processing pipeline defined in `p3iv/p3iv_modules/src/p3iv_modules/execute.py` from `p3iv/p3iv_core/src/p3iv_core/run.py/#L102`, where the argument `f_execute` is passed from `p3iv/p3iv/scripts/main.py`. Remember that the instantiation of the modules are defined in `p3iv/p3iv_modules/src/p3iv_modules/modules.py`.

While importing external modules, the simulation environment requires to follow a package name scheme. This scheme is implemented in `p3iv_modules/src/p3iv_modules/modules.py`. That is, a planner package in the workspace, besides inheriting from the metaclass interface, must have a name starting with `planner_`, whereas a prediction package's name must start with `prediction_` prefixes. Which module to use as a planner is controlled from `settings.py` file.

.. todo::
   Consider to add Python API and describe the motivation behind individual implementations.
