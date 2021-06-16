#pragma once
#include <iostream>
#include <Eigen/Core>
#include <glog/logging.h>

namespace util_probability {

template <typename T, int Dim>
struct NormalDistribution {

    using Mean = Eigen::Matrix<T, Dim, 1>;
    using Covariance = Eigen::Matrix<T, Dim, Dim>;


    NormalDistribution() : _mean{Mean::Zero()}, _covariance{Covariance::Zero()} {
    }

    NormalDistribution(const Eigen::Ref<const Mean>& mean_) : _mean{mean_}, _covariance{Covariance::Zero()} {
    }

    NormalDistribution(const Eigen::Ref<const Mean>& mean_, const Eigen::Ref<const Covariance>& covariance_)
            : _mean{mean_}, _covariance{covariance_} {
        LOG_ASSERT(_covariance.rows() == _covariance.cols());
        LOG_ASSERT(_mean.size() == _covariance.rows());
    }

    NormalDistribution(const Eigen::Ref<const Mean>& mean_, Eigen::Matrix<T, Dim, 1>& variance_)
            : _mean{mean_}, _covariance{Covariance::Zero()} {

        for (size_t i = 0; i < variance_.size(); i++) {
            _covariance(i, i) = variance_(i);
        }
    }

    size_t dimension() const {
        return static_cast<size_t>(_mean.size());
    }

    Mean mean() const {
        return _mean;
    }

    T mean(size_t r, size_t c) const {
        return _mean(r, c);
    }

    Covariance covariance() const {
        return _covariance;
    }

    T covariance(size_t r, size_t c) const {
        return _covariance(r, c);
    }

    virtual Eigen::Matrix<T, Dim, 1> variance() const {
        Eigen::Matrix<T, Dim, 1> variance;
        for (size_t i = 0; i < _covariance.rows(); i++) {
            variance(i) = _covariance(i, i);
        }
        return variance;
    }

protected:
    Mean _mean;
    Covariance _covariance;
};

} // namespace util_probability
