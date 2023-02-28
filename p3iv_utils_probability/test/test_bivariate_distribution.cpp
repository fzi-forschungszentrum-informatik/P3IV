/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <numeric>
#include <vector>
#include <glog/logging.h>
#include "bivariate_distribution.hpp"
#include "gtest/gtest.h"

using namespace util_probability;


TEST(BivariateNormalDistribution, bivariate) {

    Eigen::Matrix<double, 2, 1> mean;
    mean << 1.0, 2.0;
    Eigen::Matrix<double, 2, 2> cov;
    cov << 5.0, 1.0, 1.0, 1.0;
    BivariateNormalDistribution<double> bivariateNormal(mean, cov);

    Eigen::Matrix<double, 5, 1> ellipseParams = bivariateNormal.range(2);

    ASSERT_DOUBLE_EQ(ellipseParams(0), 1);
    ASSERT_DOUBLE_EQ(ellipseParams(1), 2);
    ASSERT_DOUBLE_EQ(ellipseParams(2), 0.23182380450040307);
    ASSERT_DOUBLE_EQ(ellipseParams(3), 4.576491222541474);
    ASSERT_DOUBLE_EQ(ellipseParams(4), 1.7480640977952844);
}


int main(int argc, char** argv) {
    ::google::InitGoogleLogging(argv[0]);
    ::google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_colorlogtostderr = true;
    FLAGS_logtostderr = true;

    return RUN_ALL_TESTS();
}
