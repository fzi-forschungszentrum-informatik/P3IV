#!/bin/sh
pip install requirements.txt
source /opt/ros/$ROS_DISTRO/setup.bash
mkdir catkin_ws && cd catkin_ws && mkdir src
catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo # build in release mode (or whatever you prefer)
cd src
git clone https://github.com/KIT-MRT/mrt_cmake_modules.git
git clone https://github.com/fzi-forschungszentrum-informatik/lanelet2.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/p3iv.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/understanding.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/polygon_geometry.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/prediction.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/util_probability.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/util_motion.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/decision_making.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/planner.git
catkin build

