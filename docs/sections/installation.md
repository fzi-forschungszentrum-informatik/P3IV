## Dependencies

P3IV is targeted towards Linux and ROS. The installation steps below are described for Ubuntu 20.04 and ROS Noetic.

### Required Dependencies

P3IV is designed to operate on top of Lanelet2 maps. Hence, the build procedure and [dependencies of Lanelet2](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/README.md#dependencies) apply to P3IV.

Further dependencies other than those for Lanelet2 are
 * `Pybind11`
 * Several python packages stored in `requirements.txt`

### Optional Dependencies

P3IV can imitate perception modules of an autonomous vehicle and can perform visible area calculations. The best way to perform these calculations is to use Computational Geometry and Algebra Library [CGAL](https://www.cgal.org/). However, CGAL has a restrictive license. Therefore, the perception module based on CGAL of the simulation environment is optional. If CMake doesn't find CGAL installed on your system, the simulation framework will fallback to matplotlib's patch-based visibility operations. This may in some cases show suboptimal performance and hence _full visibility_ can be activated from simulation settings.

A CGAL version > 5.0.3 is needed. Note that, CGAL is header-only library since v.5.0

Another optional dependency is the source of information: because drone datasets are copyrighted, they are not provided with this dataset and must be obtained separately. If you want to use some drone dataset, make sure that you have copied it into your workspace. For interaction-dataset, the default version is `v1_0`. You can modify this by revising the entry ``interaction_dataset_dir`` in [``settings.py``](https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/p3iv/p3iv_core/src/p3iv_core/configurations/settings.py).

Python implementations in P3IV are formatted with [black](https://github.com/psf/black) and C++ implementations are formatted with [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html). To match line widths of black with clang-format, the default line width is increased to 120. If prefer to continue formatting with these, you may get black and clang format on your system.

## Build

Developing an algorithm typically requires numerous builds in release and debug configurations. Binding a C++ implementation with `boost-python` or `pybind` can increase build times significantly. Therefore, it is recommended to build `Lanelet2` on a separate catkin workspace than p3iv and once it is built, to source that workspace from p3iv workspace. If you are novice, you can build lanelet2 in the same workspace as well.

In order to build a lanelet2 workspace, execute
```shell
source /opt/ros/$ROS_DISTRO/setup.bash
mkdir catkin_workspaces && cd catkin_workspaces
mkdir lanelet2_ws && cd lanelet2_ws && mkdir src
catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
cd src
git clone https://github.com/fzi-forschungszentrum-informatik/Lanelet2.git
git clone https://github.com/KIT-MRT/mrt_cmake_modules.git
cd ..
catkin build
```

After you have built, create a new workspace and source the `lanelet2_ws` by executing e.g. `source devel/setup.bash` from that lanelet2 workspace directory and execute the commands below.
```shell
$ cd ../..
$ mkdir p3iv_ws && cd p3iv_ws && mkdir src
catkin init
# build in release mode (or whatever you prefer):
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
cd src
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/p3iv.git
git clone https://github.com/KIT-MRT/mrt_cmake_modules.git
pip install -r p3iv/requirements.txt
cd ..
source ../../devel/setup.bash  # or setup.zsh
catkin build
```

.. note::
 The default path for datasets is in workspace below ``src/`` directory.

.. note::
 If you work from a new terminal, do not forget to source ROS and the both catkin workspaces.


## Docker Container

The repository contains a docker file from which you can run the simulation environment. From the repository you can
```shell
docker build -t p3iv             # builds the docker container and tags it as "p3iv"
docker run -it -rm p3iv:latest   # starts the docker image
```