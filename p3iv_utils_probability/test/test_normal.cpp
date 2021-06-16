#include <glog/logging.h>
#include "gtest/gtest.h"
#include "internal/normal.hpp"

using namespace util_probability;

TEST(NormalDistribution, defaultConstructor) {
    // create a 4x1 mean value and 4x4 cov-matrix
    NormalDistribution<double, 4> normalDistribution;
    std::cout << normalDistribution.mean() << std::endl;
}


TEST(NormalDistribution, parameterizedConstructorMean) {
    Eigen::Matrix<double, 3, 1> mean;
    mean << 1.0, 2.0, 3.0;

    NormalDistribution<double, 3> normalDistribution(mean);
    std::cout << normalDistribution.mean() << std::endl;
}


TEST(NormalDistribution, parameterizedConstructorMeanCovariance) {
    // create a 3x1 mean value and 3x3 cov-matrix

    Eigen::Matrix<double, 3, 1> mean;
    Eigen::Matrix<double, 3, 3> cov;

    NormalDistribution<double, 3> normalDistribution(mean, cov);
    std::cout << normalDistribution.covariance() << std::endl;
}


TEST(NormalDistribution, parameterizedConstructorMeanVariance) {

    Eigen::Matrix<double, 2, 1> mean;
    mean << 2.0, 3.0;
    Eigen::Matrix<double, 2, 2> cov;
    cov << 1.0, 0.0, 0.0, 2.0;

    NormalDistribution<double, 2> normalDistribution(mean, cov);
}


TEST(NormalDistribution, getCoVariance) {
    // create a 3x1 mean value and 3x3 cov-matrix

    Eigen::Matrix<double, 2, 1> mean;
    mean << 2.0, 3.0;
    Eigen::Matrix<double, 2, 2> cov;
    cov << 1.0, 0.0, 0.0, 2.0;

    NormalDistribution<double, 2> normalDistribution(mean, cov);
    std::cout << normalDistribution.variance() << std::endl;
    std::cout << normalDistribution.covariance() << std::endl;
}


TEST(NormalDistribution, dimensionQuery) {

    // create a 4x1 mean value and 4x4 cov-matrix
    NormalDistribution<double, 4> normalDistribution;
    LOG_ASSERT(normalDistribution.dimension() == 4);
}


int main(int argc, char** argv) {
    ::google::InitGoogleLogging(argv[0]);
    ::google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_colorlogtostderr = true;
    FLAGS_logtostderr = true;

    return RUN_ALL_TESTS();
}