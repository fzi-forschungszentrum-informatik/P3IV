#pragma once
#include <iostream>
#include <Eigen/Core>
#include "sequence_distribution.hpp"

namespace util_probability {


template <typename T>
struct TruncatedUnivariateNormalDistributionSequence : public UnivariateNormalDistributionSequence<T> {

    TruncatedUnivariateNormalDistributionSequence() = default;

    using Mean = Eigen::Matrix<T, Eigen::Dynamic, 1>;
    using Variance = Eigen::Matrix<T, Eigen::Dynamic, 1>;
    using Truncation = Eigen::Matrix<T, Eigen::Dynamic, 1>;

    // todo: check to pass (const std::vector<T> mean_ ...)
    TruncatedUnivariateNormalDistributionSequence(std::vector<T> mean_,
                                                  std::vector<T> variance_,
                                                  std::vector<T> upper_bound_,
                                                  std::vector<T> lower_bound_) {

        assert(mean_.size() == variance_.size());

        this->_mean = Eigen::Map<Mean>(mean_.data(), mean_.size(), 1);
        this->_covariance = Eigen::Map<Variance>(variance_.data(), variance_.size(), 1);
        this->_upper_truncation = Eigen::Map<Truncation>(upper_bound_.data(), upper_bound_.size(), 1);
        this->_lower_truncation = Eigen::Map<Truncation>(lower_bound_.data(), lower_bound_.size(), 1);
    }

    // todo: replace with range()
    std::vector<T> upperBound(const T sigma) const {

        std::vector<double> upper_bound;
        upper_bound.resize(this->_mean.size());

        for (size_t i = 0; i < upper_bound.size(); i++) {
            upper_bound[i] = std::min(_upper_truncation(i, 0), this->_mean(i, 0) + this->_covariance(i, 0) * sigma);
        }
        return upper_bound;
    }

    std::vector<T> lowerBound(const T sigma) const {

        std::vector<double> lower_bound;
        lower_bound.resize(this->_mean.size());

        for (size_t i = 0; i < lower_bound.size(); i++) {
            lower_bound[i] = std::max(_lower_truncation(i, 0), this->_mean(i, 0) - this->_covariance(i, 0) * sigma);
        }
        return lower_bound;
    }

protected:
    Truncation _upper_truncation;
    Truncation _lower_truncation;
};

} // namespace util_probability
