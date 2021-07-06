## What is P3IV for?

Motion prediction and planning for autonomous vehicles is an open research topic. Some approaches follow model-based planning methods, while others focus rely on huge amount of data and try to solve the prediction & planning problem in an end-to-end-fashion. Simulation frameworks like CARLA are well suited for to develop learning-based approaches for this task. However, from the academic perspective, these simulation frameworks have several deficiencies.

In prediction and planning research, we often require some cases that serve as a baseline to compare our proposed approach. These baselines must be well-defined and allow modifications easily. Whereas in some cases we are interested in fully hypothetical or synthetic behaviors of traffic participants, in most of the cases we would like to compare our prediction or planning results with real data. This brings the necessity to bind different, for research freely available datasets with a simulation framework.

The most interesting research question in this field is the effect of uncertainties. While evaluating newly proposed approaches, we would often like to compare our approach against different kinds and values of uncertainties. This brings the inherent need to support uncertainties in a simulation framework.

In autonomous driving research, even though the objective of the research is unique, there is a variety of approaches that lead to this objective. This aspect requires a simulation environment to be implemented in a general programming language, such as Python, in a lean way to allow for modifications. Furthermore, especially in cases where the developed algorithm needs belief tracking and update, an open-loop simulation is helpful in the early stages of experiments.

P3IV aims to address all the issues above and help the researchers with setting up baseline scenarios and serves as a framework for both open-loop and closed-loop simulation. It also presents several utility functions that ease the development of prediction and planning algorithms.

## Features of P3IV

Some important features of P3IV are listed and explained below:
  * Catkin package structure: allows clean and modular structure, seamless integration into ROS
  * Implemented in Python: allows for quick modifications and bindings to other languages such as Julia and C++ are available
  * Supports C++: even though the framework operates in Python, some underlying function and type definitions are also implemented in C++ with PyBind bindings for rapid integration of C++ implementations.
  * Allows consideration of uncertainties and limited visibility
  * Inherently supports advanced the map data library Lanelet2: utilization of HD offline maps, routing functionalities, intersection calculations
  * Inherently supports real world drone datasets, such as INTERACTION Dataset
  * Allows both open-loop and closed-loop simulation
  * Contains modular visualization functions that can be easily combined in application-specific plots
  * Released under the BSD 3-Clause license.

## What is P3IV not?

If you consider using P3IV for your research, you should be aware of what this framework is not intended to do with.

First, if you plan to do large scale integration tests rather than developing entirely new algorithms for research, you should rather consider to use Deepdrive, CARLA, LGSVL, Carmaker, Coincarsim (...). This simulation environment is not aimed for Hardware-in-the-loop testing or testing with commercially available sensor models. Furthermore, it doesn't provide any photorealistic environment. Its focus is processing chain, after environment perception.

Real time simulation frameworks share information among its modules and components typically with timestamped messages (cf. [ROS messages](http://wiki.ros.org/msg)). Upon processing these messages must be extrapolated and aligned in time. Because such operations are rather engineering tasks and do not bring any further value to the developed algorithm, we _freeze_ the time while processing. Processing time of individual modules can be measured in a stand-alone basis. If you plan to do integration tests while covering processing delays and jitters, you should use another simulation framework.

P3IV has been developed with a focus on vehicle-to-vehicle interactions. Therefore, we do not support cyclists or pedestrians yet. But the modular structure of the framework allows such an extension, and we plan to integrate cyclists and pedestrians.
