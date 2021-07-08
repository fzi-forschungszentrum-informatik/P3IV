/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include "internal/normal.hpp"

namespace util_probability {


template <typename T>
class BivariateNormalDistribution : public NormalDistribution<T, 2> {
public:
    BivariateNormalDistribution() = default;

    explicit BivariateNormalDistribution(T meanX, T meanY) {
        this->_mean << meanX, meanY;
    }

    BivariateNormalDistribution(T meanX, T meanY, T covXX, T covXY, T covYX, T covYY) {
        this->_mean << meanX, meanY;
        this->_covariance << covXX, covXY, covYX, covYY;
    }

    void setCovariance(T covXX, T covXY, T covYX, T covYY) {
        this->_covariance << covXX, covXY, covYX, covYY;
    }

    void setMean(T meanX, T meanY) {
        this->_mean << meanX, meanY;
    }

    std::vector<T> range(const double& n) const {

        std::vector<T> rangeValues;
        rangeValues.resize(5);

        // todo: calculate ellipse parameters

        return rangeValues;
    }
};
} // namespace util_probability