#pragma once
#include "p3iv_utils_probability/bivariate_distribution.hpp"
#include "p3iv_utils_probability/sequence_distribution.hpp"
#include "p3iv_utils_probability/univariate_distribution.hpp"

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


struct MotionStateArray {

    MotionStateArray() {
        position = BivariateNormalDistributionSequence<double>();
        yaw = UnivariateNormalDistributionSequence<double>();
        velocity = BivariateNormalDistributionSequence<double>();
    }

    BivariateNormalDistributionSequence<double> position;
    UnivariateNormalDistributionSequence<double> yaw;
    BivariateNormalDistributionSequence<double> velocity;
};


} // namespace p3iv_types