## Dependencies

P3IV is targeted towards Linux and ROS. The installation steps below are described for Ubuntu 20.04 and ROS Noetic.

### Required Dependencies

P3IV is designed to operate on top of Lanelet2 library. Because Lanelet2 is a dependency of P3IV, the build procedure and [dependencies of Lanelet2](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/README.md#dependencies) apply to P3IV.

Further dependencies other than those for Lanelet2 are
 * `Pybind11`
 * Several python packages stored in `requirements.txt`

### Optional Dependencies

In autonomous driving applications as well as in this simulation framework, obtaining high precision in real-time is a topic of primary concern. For this reason, P3IV implements core functions in C++ and provides either a Python api or their Python counterparts.

P3IV can imitate perception modules of an autonomous vehicle and can perform visible area calculations. Such calculations can be performed with polygon clipping libraries, for which many alternatives are available. The most reliable and fastest way to perform these calculations is to use Computational Geometry and Algebra Library [CGAL](https://www.cgal.org/) which is implemented in C++.

CGAL has a restrictive license limiting its commercial use. Even though P3IV sets its focus on academic research, it sets the perception module which depends on CGAL as optional. If CMake doesn't find CGAL installed on your system, the simulation framework will fall back to perfect visibility, assuming an unlimited sensor range.

.. warning::
   A CGAL version > v5.0.3 is needed. CGAL is header-only library since v5.0. Ubuntu package manager provides v4.x for 18.04 and v5.x for Ubuntu 20.04.

Another optional dependency is the source of information: because drone datasets are copyrighted, they are not provided with this dataset and must be obtained separately. If you want to use some drone dataset, make sure that you have copied it below ``src/`` directory of your workspace. For interaction-dataset, the default version is `v1_0`. You can modify this by revising the entry ``dataset`` in ``settings.yaml`` (*cf.* :ref:`usage Configurations` for more information).

Python implementations in P3IV are formatted with [black](https://github.com/psf/black) and C++ implementations are formatted with [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html). To match line widths of black with clang-format, the default line width is increased to 120. If prefer to continue formatting with these, you may get black and clang format on your system (*cf.* :ref:`faq Building` for more information).

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
git clone https://github.com/fzi-forschungszentrum-informatik/P3IV.git
git clone https://github.com/KIT-MRT/mrt_cmake_modules.git
pip install -r p3iv/requirements.txt
cd ..
source ../../devel/setup.bash  # or setup.zsh
catkin build
```

.. note::
 If you work from a new terminal, do not forget to source ROS and the both catkin workspaces.


## Docker Container

The repository contains a docker file from which you can run the simulation environment. From the repository you can
```shell
docker build -t p3iv             # builds the docker container and tags it as "p3iv"
docker run -it -rm p3iv:latest   # starts the docker image
```