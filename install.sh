#!/bin/sh
pip install -r requirements.txt
cd ..
git clone https://gitlab.mrt.uni-karlsruhe.de/pub/mrt_cmake_modules.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/understanding.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/polygon_geometry.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/prediction.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/util_probability.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/util_motion.git
git clone https://gitlab.mrt.uni-karlsruhe.de/planning-simulation/planner.git