# P3IV

Main pkg for Probabilistic Prediction and Planning for Intelligent Vehicles (P3IV) Simulator

### [Doxygen documentation](http://mrt.pages.mrt.uni-karlsruhe.de/planning-simulation/p3iv/doxygen/index.html)
### [Coverage report](http://mrt.pages.mrt.uni-karlsruhe.de/planning-simulation/p3iv/coverage/index.html)

## Usage

  * Ensure you have `INTERACTION-Dataset-DR-v1_1` in your workspace.
  * Test-cases are inside `p3iv/src/p3iv/configurations/test_cases.py`
  * Run the simulation by running `main.py` in `scripts/` and specifying a test-case.
  * If you have any problem, get help with `python main.py --help`.

```
python main.py --predict=DEU_Roundabout_OL_01
python main.py --run=DEU_Roundabout_OL_01

```
## Install

```
#!/bin/sh
pip install requirements.txt
source /opt/ros/$ROS_DISTRO/setup.bash
mkdir catkin_ws && cd catkin_ws && mkdir src
catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo # build in release mode (or whatever you prefer)
```

```
git clone https://gitlab.mrt.uni-karlsruhe.de/pub/mrt_cmake_modules.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/understanding.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/polygon_geometry.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/prediction.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/util_probability.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/util_motion.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/decision_making.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/planner.git
```