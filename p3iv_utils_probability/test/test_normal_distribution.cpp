/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <numeric>
#include <vector>
#include <glog/logging.h>
#include "univariate_distribution.hpp"
#include "gtest/gtest.h"

using namespace util_probability;


TEST(UnivariateNormalDistribution, defaultConstructor) {
    UnivariateNormalDistribution<double> foo;
    std::cout << foo.mean() << std::endl;
}


TEST(UnivariateNormalDistribution, vectorConstructorSingle) {

    double v_mean = 3.0;
    double v_variance = 1.0;
    UnivariateNormalDistribution<double> u_normal_dist(3, 1);

    ASSERT_DOUBLE_EQ(3, u_normal_dist.mean()[0]);
    ASSERT_DOUBLE_EQ(1, u_normal_dist.variance()[0]);
    ASSERT_DOUBLE_EQ(1, u_normal_dist.covariance()[0]);
    ASSERT_DOUBLE_EQ(1, u_normal_dist.dimension());
    ASSERT_DOUBLE_EQ(2, u_normal_dist.range(1.0)[0]);
    ASSERT_DOUBLE_EQ(4, u_normal_dist.range(1.0)[1]);
}


int main(int argc, char** argv) {
    ::google::InitGoogleLogging(argv[0]);
    ::google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_colorlogtostderr = true;
    FLAGS_logtostderr = true;

    return RUN_ALL_TESTS();
}
