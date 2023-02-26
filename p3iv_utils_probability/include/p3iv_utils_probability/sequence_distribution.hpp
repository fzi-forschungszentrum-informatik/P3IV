/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include <iostream>
#include <Eigen/Core>

namespace util_probability {


/**
 * @brief: Container for n-dimensional normal distributions
 *
 */
template <typename T, int DistributionDim>
struct NormalDistributionSequence {
    using Mean = Eigen::Matrix<T, Eigen::Dynamic, DistributionDim>;
    using Covariance = Eigen::Matrix<T, Eigen::Dynamic, DistributionDim>;


    NormalDistributionSequence() = default;

    NormalDistributionSequence(const Eigen::Ref<const Mean>& mean_, const Eigen::Ref<const Covariance>& covariance_)
            : _mean{mean_}, _covariance{covariance_} {
    }

    NormalDistributionSequence(const Eigen::Ref<const Mean>& mean_, Eigen::Matrix<T, Eigen::Dynamic, 1>& variance_)
            : _mean{mean_}, _covariance{Covariance::Zero()} {

        for (size_t i = 0; i < variance_.size(); i++) {
            _covariance(i, i) = variance_(i);
        }
    }

    NormalDistributionSequence(std::vector<T> mean_, std::vector<T> covariance_) {
        _mean = Eigen::Map<Mean, Eigen::Unaligned>(mean_.data(), mean_.size() / DistributionDim, DistributionDim);
        _covariance = Eigen::Map<Covariance, Eigen::Unaligned>(
            covariance_.data(), covariance_.size() / DistributionDim, DistributionDim);
    };

    size_t dimension() const {
        return static_cast<size_t>(_mean.size() / DistributionDim);
    }

    void setMean(std::vector<T> mean_) {
        _mean = Eigen::Map<Mean, Eigen::Unaligned>(mean_.data(), mean_.size() / DistributionDim, DistributionDim);
    }

    void setCovariance(std::vector<T> covariance_) {
        _covariance = Eigen::Map<Mean, Eigen::Unaligned>(
            covariance_.data(), covariance_.size() / DistributionDim, DistributionDim);
    }

    Mean mean() const {
        return _mean;
    }

    Covariance covariance() const {
        return _covariance;
    }

    std::vector<T> meanVec() {
        std::vector<T> mean(_mean.data(), _mean.data() + _mean.rows() * _mean.cols());
        return mean;
    }

    T covariance(size_t r, size_t c) const {
        return _covariance(r, c);
    }


protected:
    Mean _mean;
    Covariance _covariance;
};


/**
 * @brief: Container for univariate normal distributions
 *
 */
template <typename T>
struct UnivariateNormalDistributionSequence : NormalDistributionSequence<T, 1> {
    using Mean = Eigen::Matrix<T, Eigen::Dynamic, 1>;
    using Covariance = Eigen::Matrix<T, Eigen::Dynamic, 1>;

    using NormalDistributionSequence<T, 1>::NormalDistributionSequence;
    using NormalDistributionSequence<T, 1>::mean;
    using NormalDistributionSequence<T, 1>::covariance;

    T mean(size_t e) const {
        return this->_mean(e, 0);
    }

    T covariance(size_t e) const {
        return this->_covariance(e, 0);
    }
};


/**
 * @brief: Container for bivariate normal distributions
 *
 * Cross correlation terms are set to zero.
 */
template <typename T>
struct BivariateNormalDistributionSequence : NormalDistributionSequence<T, 2> {
    using Mean = Eigen::Matrix<T, Eigen::Dynamic, 2>;
    using Covariance = Eigen::Matrix<T, Eigen::Dynamic, 4>;

    using NormalDistributionSequence<T, 2>::NormalDistributionSequence;

    BivariateNormalDistributionSequence(const Eigen::Ref<const Mean>& mean_,
                                        Eigen::Matrix<T, Eigen::Dynamic, 1>& variance_)
            : NormalDistributionSequence<T, 2>(mean_, Covariance::Zero()) {

        for (size_t i = 0; i < this->dimension(); i++) {
            this->_covariance(i, 0) = variance_(i);
            this->_covariance(i, 3) = variance_(i);
        }
    }

    using NormalDistributionSequence<T, 2>::mean;
    using NormalDistributionSequence<T, 2>::covariance;

    T mean(size_t e, size_t c) const {
        return this->_mean(e, c);
    }

    T covariance(size_t e, size_t c) const {
        return this->_covariance(e, c);
    }

    virtual Eigen::Matrix<T, Eigen::Dynamic, 2> variance() const {
        Eigen::Matrix<T, Eigen::Dynamic, 2> variance;
        for (size_t i = 0; i < this->dimension(); i++) {
            variance(i, 0) = this->_covariance(i, 0);
            variance(i, 1) = this->_covariance(i, 3);
        }
        return variance;
    }
};


} // namespace util_probability