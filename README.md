# P3IV Simulator

Probabilistic Prediction and Planning for Intelligent Vehicles (P3IV) Simulator is a simulation framework for motion prediction and planning for autonomous vehicles.

## What is P3IV for?

Motion prediction and planning for autonomous vehicles is an open research topic. Some approaches follow model based planning methods, while others focus rely on huge amount of data and try to solve the prediction & planning problem in an end-to-end-fashion. Simulation frameworks like CARLA are well suited for to develop learning-based approaches for this task. However, from academic perspective these simulation frameworks have several deficiencies.

In prediction and planning research, we often require some cases that serve as a baseline to compare our proposed approach. These baselines must be well-defined and allow modifications easily. Whereas in some cases, where we are interested in fully hypothetical or synthetic behaviors of traffic participants, in most of the cases, we would like to compare our prediction or planning results with real data. This brings the necessity to bind different, for research freely available datasets with a simulation framework.

The most interesting research question in this field are the effect of uncertainties. While evaluating newly proposed approaches, we would often like to compare our approach against different kinds and values of uncertainties. This brings the inherent need to support uncertainties in a simulation framework.

In autonomous driving research, even though the objective of the research is unique, there is a variety of approaches that lead to this objective. This aspect requires to a simulation environment to be implemented in a general programming language, such as Python, in a lean way to allow for modifications. Furthermore, especially in cases where the developed algorithm needs belief tracking and update, an open-loop simulation is helpful in the early stages of experiments. 

P3IV aims to address all the issues above and help the researchers with setting up baseline scenarios and serves as a framework for both open-loop and closed-loop simulation. It also presents several utility functions that ease the development of prediction and planning algorithms. 

## Features of P3IV

Some important features of P3IV are listed and explained below:
  * Catkin package structure: allows clean and modular structure, seamless integration into ROS
  * Implemented in Python: allows for quick modifications and bindings to other languages such as Julia and C++ are available
  * Supports C++: even though the framework operates in Python, some underlying function and type definitions are also implemented in C++ with PyBind bindings for rapid integration of C++ implementations.
  * Allows consideration of uncertainties and limited visibility
  * Inherently supports advanced the map data library Lanelet2: utilization of HD offline maps, routing functionalities, intersection calculations
  * Inherently supports real world drone datasets, such as INTERACTION Dataset
  * Contains modular visualization functions that can be easily combined in application-specific plots
  * Released under the BSD 3-Clause license.

## What is P3IV not?

If you consider to use P3IV for your research, you should be aware of what this framework is not intended to do with.

First, if you plan to do large scale integration tests, rather than developing entirely new algorithms for research, you should rather consider to use Deepdrive, CARLA, LGSVL, Carmaker, Coincarsim (...). This simulation environment is not aimed for Hardware-in-the-loop testing or testing with commercially available sensor models. It further doesn't provide any photorealistic environment. Its focus is processing chain, after environment perception.

Real time simulation frameworks, share information among its modules and components typically with timestamped messages (cf. ROS messages). Upon processing these messages must be extrapolated and aligned in time. Because such operations are rather engineering tasks and do not bring any further value to the developed algorithm, we _freeze_ the time while processing. Processing time of individual modules can be measured in a stand-alone basis. If you plan to do integration tests while covering processing delays and jitters, you should use another simulation framework.  

P3IV has been developed with a focus on vehicle to vehicle interactions. Therefore, we do not support cyclists or pedestrians yet. But the modular structure of the framework allows such an extension, and we plan to integrate cyclists and pedestrians.

## Installation

P3IV is targeted towards Linux and ROS. The installation steps below are described for Ubuntu 18.04 and ROS Melodic. 


### Required Dependencies

P3IV is designed to operate on top of Lanelet2 maps. Hence, the build procedure and dependencies of Lanelet2 apply to P3IV.

Other required dependencies are
 * `Pybind11`
 * Several python packages stored in `requirements.txt`

### Optional Dependencies

P3IV can imitate perception modules of an autonomous vehicle and can perform visible area calculations. The best way to perform these calculations is to use Computational Geometry and Algebra Library [CGAL](https://www.cgal.org/). However, CGAL has a restrictive license. Therefore, the perception module based on CGAL of the simulation environment is optional. If CMake doesn't find CGAL installed on your system, the simulation framework will fallback to matplotlib's patch-based visibility operations. This may in some cases show suboptimal performance and hence _full visibility_ can be activated from simulation settings. 

A CGAL version > 5.0.3 is needed. Note that, CGAL is header-only library since v.5.0

Another optional dependency is the source of information: because drone datasets are copyrighted, they are not provided with this dataset and must be obtained separately. If you want to use some drone dataset, make sure that you have copied it into your workspace. For interaction-dataset, the default version is `v1_0`. You can modify this by revising the entry `interaction_dataset_dir` in [`settings.py`](https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/p3iv/p3iv_core/src/p3iv_core/configurations/settings.py).

Python implementations in P3IV are formatted with [black](https://github.com/psf/black) and C++ implementations are formatted with [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html). To match line widths of black with clang-format, the default line width is increased to 120. If prefer to continue formatting with these, you may get black and clang format on your system.

### Recommended Build

Developing an algorithm typically requires numerous builds in release and debug configurations. Binding a C++ implementation with `boost-python` or `pybind` can increase build times significantly. Therefore, it is recommended to build `Lanelet2` on a separate catkin workspace than p3iv and once it is built, to source that workspace from p3iv workspace. If you are novice, you can build lanelet2 in the same workspace as well.

In order to build you lanelet2 workspace, execute
```
source /opt/ros/$ROS_DISTRO/setup.bash
mkdir catkin_workspaces && cd catkin_workspaces && mkdir lanelet2_ws && cd lanelet2_ws && mkdir src
catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
cd src
git clone https://github.com/fzi-forschungszentrum-informatik/Lanelet2.git
cd ..
catkin build
```

After you have built, create a new workspace and source the `lanelet2_ws` and pull the simulation environment.
```
cd ../..
mkdir p3iv_ws && cd p3iv_ws && mkdir src
catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo # build in release mode (or whatever you prefer)
cd src
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/p3iv.git
pip install -r p3iv/requirements.txt
chmod +x p3iv/install.sh
./p3iv/install.sh
cd ..
source ../../devel/setup.bash  # or zsh
catkin build
```

## Usage

The simulation framework can be executed as 
```
cd p3iv/p3iv/scripts
python main.py --run=DEU_Roundabout_OL_01
```

This command executes the test case `DEU_Roundabout_OL_01` defined inside `p3iv/src/p3iv/configurations/test_cases.py`. You can add more test cases, depending on your need. 

If you have any problems and need help, execute
```
python main.py --help
``` 
If you want to display inspect the results of a simulation, you can either execute
```
python main.py --show-single=<TIMESTAMP_VALUE>
``` 
or
```
python main.py --show-multi
``` 
These commands will start animations on the outcomes of planned trajectories. The first command will animate the planning results for a single timestamp <TIMESTAMP_VALUE> by iterating over individual timesteps, whereas the latter will iterate over all the timestamps at which planning is performed and will animate these.

## Customization

Researchers frequently have to adapt the simulation setting to match the needs of their application. Even though, the framework has a clean layout, it may still be confusing for inexperienced researchers in python, catkin, or cmake.  


### Layout of the packages

P3IV works in a [catkin workspace](https://wiki.ros.org/catkin) and follows the catkin package layout. In a catkin package any python module or subpackage a sourced environment can find is located below `<PACKAGE_NAME>/src/<PACKAGE_NAME>`. After build, modules can be imported as `from <PACKAGE_NAME> import <MODULE_NAME>.

Packages have test cases for coverage and CI testing. These tests are located inside `<PACKAGE_NAME>/test/` directory. Even though, these tests are implemented for testing, they can serve as exemplary use of functions and types. 

The simulation framework is shipped as a catkin metapackage, e.g. a package that contains multiple other packages. The scripts to execute the framework are located in `p3iv/p3iv`, in `scripts` directory. After each simulation run, the outputs are stored inside this directory with the directory names reflecting the start time of the simulation run.

The core functions to run the environment are inside `p3iv/p3iv_core`. Bindings to data sources such as drone datasets and configurations of the simulation framework are located in this package.

The simulation framework instantiates a vehicle with perception, understanding, decision making, planning and action (or control) modules. Default or exemplary modules are located inside `p3iv/p3iv_modules`. A vehicle instantiates the modules located inside `p3iv/p3iv_modules/src/p3iv_modules/modules.py` and calls them sequentially for every timestamp. These modules calculate the required output, such as predicted motion of other vehicles around for every *timestep* in the planning horizon.

The framework operates with certain classes of datatypes. The datatypes serve both as baseline and as a guideline for future improvements. These are located inside `p3iv/p3iv_types`. Note that, this package has also type implementations for C++ and their PyBind bindings for Python-use.

While developing algorithms, researchers frequently need some common functions. Most of the time, such functions are implemented in various libraries. However, some application specific utilities are sometimes hard to fine. `p3iv/p3iv_utilities` contains a small amount of useful functions.

Visualization can guide researchers for possible improvements and help with debugging. Because there isn't a single visualization that depicts all possible metrics, visualization is implement in an object-oritented fashion but in a very modular way. Every visualization function is a class, that can accept instances of others, e.g. Cartesian plot instantiates the class that depicts vehicles and the class that depict a Lanelet2 map. Such functions are located inside `p3iv/p3iv_visualization`.


### Simulation configurations

In P3IV there two types of configurations that a user can modify. The first one is test cases. These are located inside `p3iv/p3iv_core/src/p3iv_core/configurations/test_cases.py`. This file contains a dictionary with key representing names that can be used an argument for the main script, e.g. `python main.py --run=<TEST_CASE_KEY>`. Every test case specifies the begin and end timestamps of the simulation, the ID of the ego (or host) vehicle. With the key `planning_meta`, it specifies as a dictionary with keys representing the IDs of the vehicle where the vehicle is heading to and with values both the lanelet ID where that heading to and the type of planner the vehicle with that ID is heading to. All vehicle IDs defined in `planning_meta` do closed-loop simulation. In other words, they react to the changes in the simulation environment.

The second configuration is the simulation settings, located in `p3iv/p3iv_core/src/p3iv_core/configurations/settings.py`. This defines parameters such as planning horizon, location of a drone dataset, levels of uncertainty. Therefore, whereas the former one, `test_cases.py` describe the test scene, this describes the individual parameters of the test scenario.

Independent of the defined configurations in these two files, every module written by the users can contain other configuration files. This is up to the user. The users can also modify and extend these settings to match their needs.

### Data processing structure of the framework

The simulation framework runs staring from `timestamp_begin` defined in `test_cases.py` and finishes at `timestamp_end` defined in the same file. It sequentially executes the modules and returns the output. If the `simulation_type` is closed-loop, it updates its current position based on the planned value. An open-loop usage requires presence of a dataset, as it reads data from such a source to update for the next timestamp.

Upon execution, the simulation framework starts sequentially executing the processing pipeline defined in `p3iv/p3iv_modules/src/p3iv_modules/execute.py` from `p3iv/p3iv_core/src/p3iv_core/run.py/#L102`, where the argument `f_execute` is passed from `p3iv/p3iv/scripts/main.py`. Remember that the instantiation of the modules are defined in `p3iv/p3iv_modules/src/p3iv_modules/modules.py`.


### Overview on the data types and modules

The simulation framework is aimed to have a modular structure and to work with flexibly with various ROS packages and modules. Catkin package layout and CMake meets this requirement perfectly. Nevertheless, for these different modules to work with each other, interfaces or messages must be predefined.

Indicated in the Section  [_"What P3IV is not?"_](##What-is-P3IV-not?) we do not define messages with timestamps. But for modules to operate with each other, we define interfaces as metaclasses and some data types. The interfaces are placed inside `p3iv/p3iv_modules/src/p3iv_modules/interfaces/` and the data types are placed inside `p3iv/p3iv_types/`. A check on whether instantiated modules follow the interfaces is done in class `VehicleModules`, located inside `p3iv_modules/src/p3iv_modules/modules.py`. A user is free to modify and extend these data types and interfaces. Note that some modules may have modified `__init__.py` files, as in the case of `p3iv/p3iv_modules/src/p3iv_modules/interfaces/`.

While importing external modules, the simulation environment requires to follow a package name scheme. This scheme is implemented in `p3iv_modules/src/p3iv_modules/modules.py`. That is, a planner package in the workspace, besides inheriting from the metaclass interface, must have a name starting with `planner_`, whereas a prediction package's name must start with `prediction_` prefixes. Which module to use as a planner is controlled from `settings.py` file.

## Utility Functions

P3IV contains utility functions that are frequently used for motion prediction and planning. These functions do not have any dependency to other packages and can be used off-the-shelf. These are located inside the package `p3iv_utils`. Among others, utility functions implemented consist of
 * Driver models
 * Finite difference calculations
 * Lanelet2 map reader function
 * Color-print function for console prints
 * Vehicle rectangle function
 * Functions to calculate extrema motion

Apart from the package `p3iv_utils`, there are additional packages whose name start with `p3iv_utils_` prefix. They also serve for utility functionalities and have a readme file describing their functionalities.
## FAQ

You can find answers to frequently asked questions below.

 * Simulation framework fails to find a package or a module. Why?
   * Please ensure that you have built and sourced your workspace in the terminal you run the simulation environment. In case, refer search for keywords _ros catkin workspace source_ on the internet.
 * For which type of application would you recommend p3iv most?
   * This is up to you. No matter if you are developing Dynamic Bayesian networks for prediction or model based planning methods such as mpc-planner, you can use this simulation framework. But if you do reinforcement learning, you may prefer to limit your use to some utility functions.
 * How can I set up this simulation framework in VS Code?
    * It's always a good idea to run some Python code in an IDE: adding breakpoints to unclear places helps to reveal the types and to understand the processing. You may add the lines below to your `launch.json` file.
        ```
        "configurations": [
            {
                "name": "DEU_Roundabout_OL_01",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/src/p3iv/p3iv/scripts/main.py",
                "cwd": "${workspaceFolder}/src/p3iv/p3iv/scripts",
                "args": [
                    "DEU_Roundabout_OL_01",
                    "--run"
                ],
                "console": "internalConsole"
            }
        ]
        ```
    * If you want to modify line width of black, you may add the lines below to your `settings.json` file.
        ```
        "python.formatting.provider": "black",
        "python.formatting.blackPath": "<BLACK_INSTALL_DIR>/bin/black",
        "python.formatting.blackArgs": [
            "--line-length",
            "120"
        ]        ```
* Is it possible to create videos from results?
  * Yes, the animation figures are named during saving in such a way that, they can be used to create a video file. For this, ensure that you have installed ``ffmpeg` on your computer and then change to the outputs directory you want to create a video. Execute the command `ffmpeg -r 5 -i step_%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4`.

## Citation

I haven't published the simulation framework as publication yet. Still, I would appreciate a citation if you use this framework or a utility function part of it in your research. You can use `bibtex` entry below.
```
@misc{p3iv,
  title = {P3IV: Probabilistic Prediction and Planning Simulator for Intelligent Vehicles},
  author = {Ömer Sahin Tas},
  year = {2021},
  note = {unpublished software}
}
```
## Misc
 * [Doxygen documentation](http://mrt.pages.mrt.uni-karlsruhe.de/planning-simulation/p3iv/doxygen/index.html)
 * [Coverage report](http://mrt.pages.mrt.uni-karlsruhe.de/planning-simulation/p3iv/coverage/index.html)