#pragma once
#include "util_probability/bivariate_distribution.hpp"
#include "util_probability/sequence_distribution.hpp"
#include "util_probability/univariate_distribution.hpp"

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


template <int Dim>
struct MotionStateArray {

    MotionStateArray() {
        position = BivariateNormalDistributionSequence<double, Dim>();
        yaw = UnivariateNormalDistributionSequence<double, Dim>();
        velocity = BivariateNormalDistributionSequence<double, Dim>();
    }

    BivariateNormalDistributionSequence<double, Dim> position;
    UnivariateNormalDistributionSequence<double, Dim> yaw;
    BivariateNormalDistributionSequence<double, Dim> velocity;
};


} // namespace p3iv_types