# P3IV

Main pkg for Probabilistic Prediction and Planning for Intelligent Vehicles (P3IV) Simulator

### [Doxygen documentation](http://mrt.pages.mrt.uni-karlsruhe.de/planning-simulation/p3iv/doxygen/index.html)
### [Coverage report](http://mrt.pages.mrt.uni-karlsruhe.de/planning-simulation/p3iv/coverage/index.html)

## Usage

  * Test-cases are inside `p3iv/src/p3iv/configurations/test_cases.py`
  * Run the simulation by running `main.py` in `scripts/` and specifying a test-case.
  * If you have any problem, get help with `python main.py --help`.

```
python main.py --predict=DEU_Roundabout_OL_01
python main.py --run=DEU_Roundabout_OL_01

```
## Install


```
source /opt/ros/$ROS_DISTRO/setup.bash
mkdir catkin_ws && cd catkin_ws && mkdir src
catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo # build in release mode (or whatever you prefer)
```

Ensure you have cloned all the dependencies into your workspace. You can execute `install.sh` for this. You may need to make it executable with `chmod +x install.sh` first. 

If you want to use drone data, make sure that you have copied it into your workspace. For interaction-dataset, the default version is `v1_0`. You can modify this by revising the entry `interaction_dataset_dir` in (`settings.py`)[p3iv/p3iv_core/src/p3iv_core/configurations/settings.py].

