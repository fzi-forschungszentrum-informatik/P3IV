====
P3IV
====

Probabilistic Prediction and Planning for Intelligent Vehicles (P3IV) Simulator is a simulation framework for motion prediction and planning of autonomous vehicles.

Focus:
  - Algorithm development for prediction and planning
  - Consideration of uncertainties and limited visibility
  - Multi-agent interactions
  - Provides utility libraries for prediction and planning
  - Allows both open-loop and closed-loop simulation

.. image:: graphics/p3iv.gif
  :width: 600
  :align: center
  :alt: P3IV visualization

Key features:
  - Catkin package structure: seamless integration into ROS
  - Implemented in Python and C++; wrapped with PyBind
  - Build on the HD map library Lanelet2
  - Bindings to simulate with real-world drone datasets
  - BSD 3-Clause license


.. toctree::
   :caption: Overview
   :hidden:
   :maxdepth: 3

   sections/overview

.. toctree::
   :caption: Installation
   :hidden:
   :maxdepth: 2

   sections/installation

.. toctree::
   :caption: Usage
   :hidden:
   :maxdepth: 2

   sections/usage

.. toctree::
   :caption: Utility Functions
   :maxdepth: 1
   :hidden:

   sections/utility

.. toctree::
   :caption: FAQ
   :maxdepth: 2
   :hidden:

   sections/faq

.. toctree::
   :caption: Misc
   :maxdepth: 2
   :hidden:


   sections/misc
