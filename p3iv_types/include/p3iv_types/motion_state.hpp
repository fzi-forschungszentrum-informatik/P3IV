#pragma once
#include "util_probability/distributions.hpp"

namespace p3iv_types {

using namespace util_probability;


struct MotionState {

    MotionState() {
        position = BivariateNormalDistribution<double>();
        yaw = UnivariateNormalDistribution<double>();
        velocity = BivariateNormalDistribution<double>();
    }

    BivariateNormalDistribution<double> position;
    UnivariateNormalDistribution<double> yaw;
    BivariateNormalDistribution<double> velocity;
};


} // namespace p3iv_types