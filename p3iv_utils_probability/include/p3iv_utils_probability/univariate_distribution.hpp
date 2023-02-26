/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include "internal/normal.hpp"

namespace util_probability {


template <typename T>
class UnivariateNormalDistribution : public NormalDistribution<T, 1> {
public:
    UnivariateNormalDistribution() = default;

    explicit UnivariateNormalDistribution(T mean) {
        this->_mean << mean;
    }

    UnivariateNormalDistribution(T mean, T cov) {
        this->_mean << mean;
        this->_covariance << cov;
    }

    void setCovariance(T cov) {
        this->_covariance << cov;
    }

    void setMean(T mean) {
        this->_mean << mean;
    }

    std::vector<T> range(const double& n) const {

        std::vector<T> rangeValues;
        rangeValues.resize(2);

        rangeValues[0] = this->_mean(0, 0) - this->_covariance(0, 0) * n;
        rangeValues[1] = this->_mean(0, 0) + this->_covariance(0, 0) * n;

        return rangeValues;
    }
};

} // namespace util_probability