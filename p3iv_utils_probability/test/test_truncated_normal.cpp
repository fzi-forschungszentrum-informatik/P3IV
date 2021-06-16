#include <numeric>
#include <vector>
#include <glog/logging.h>
#include "truncated_distribution.hpp"
#include "gtest/gtest.h"

using namespace util_probability;


TEST(TruncatedUnivariateNormalDistributionSequence, defaultConstructor) {
    TruncatedUnivariateNormalDistributionSequence<double> foo;
}

TEST(TruncatedUnivariateNormalDistributionArray, truncation) {

    const int v_size = 4;

    std::vector<double> v_mean;
    v_mean.push_back(3);
    v_mean.push_back(4);
    v_mean.push_back(5);
    v_mean.push_back(6);

    std::vector<double> v_variance(v_size, 2);
    std::vector<double> upper_truncation(v_size, 6);
    std::vector<double> lower_truncation(v_size, 3);

    TruncatedUnivariateNormalDistributionSequence<double> tr_normal(
        v_mean, v_variance, upper_truncation, lower_truncation);

    std::vector<double> expected_mean{3, 4, 5, 6};
    std::vector<double> expected_upper_bound{5, 6, 6, 6};
    std::vector<double> expected_lower_bound{3, 3, 3, 4};

    for (int i = 0; i < v_size; ++i) {
        ASSERT_DOUBLE_EQ(expected_mean[i], tr_normal.mean()[i]);
        ASSERT_DOUBLE_EQ(expected_mean[i], tr_normal.meanVec()[i]);
        ASSERT_DOUBLE_EQ(expected_upper_bound[i], tr_normal.upperBound(1.0)[i]);
        ASSERT_DOUBLE_EQ(expected_lower_bound[i], tr_normal.lowerBound(1.0)[i]);
    }
}


int main(int argc, char** argv) {
    ::google::InitGoogleLogging(argv[0]);
    ::google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_colorlogtostderr = true;
    FLAGS_logtostderr = true;

    return RUN_ALL_TESTS();
}