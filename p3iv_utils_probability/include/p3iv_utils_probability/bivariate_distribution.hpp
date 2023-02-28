/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include <cmath>
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

    Eigen::Matrix<double, 5, 1> range(const double& n) const {

        // calculate ellipse parameters
        Eigen::Matrix<double, 3, 1> ellipseParams = getEllipseParameters(2);

        // rangeValues: x, y, theta, ell_radius_x, ell_radius_y
        Eigen::Matrix<double, 5, 1> rangeValues;
        rangeValues << this->_mean, ellipseParams;

        return rangeValues;
    }

protected:
    Eigen::Matrix<double, 3, 1> getEllipseParameters(const double& n) const {

        // calculate eigenvalues
        Eigen::Matrix<double, 2, 1> eivals = this->_covariance.eigenvalues().real();

        // calculate eigenvectors
        Eigen::EigenSolver<Eigen::Matrix<double, 2, 2>> eigensolver(this->_covariance);
        Eigen::Matrix<double, 2, 1> c = eigensolver.eigenvectors().real().col(0);
        double theta = std::atan2(c(1), c(0));

        // pack the values in a vector
        Eigen::Matrix<double, 3, 1> ellipseParams;
        ellipseParams(0) = theta;
        ellipseParams(1) = n * sqrt(eivals(0));
        ellipseParams(2) = n * sqrt(eivals(1));

        return ellipseParams;
    }
};
} // namespace util_probability