/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <numeric>
#include <vector>
#include <glog/logging.h>
#include "sequence_distribution.hpp"
#include "gtest/gtest.h"

using namespace util_probability;


TEST(NormalDistributionSequence, defaultConstructor) {
    UnivariateNormalDistributionSequence<double> uniNormal;
    BivariateNormalDistributionSequence<double> biNormal{};
}


TEST(UnivariateNormalDistributionSequence, vectorConstructor) {
    std::vector<double> vMean;
    vMean.push_back(3);
    vMean.push_back(4);
    vMean.push_back(5);
    vMean.push_back(6);
    std::vector<double> vVariance(4, 1);

    UnivariateNormalDistributionSequence<double> uniNormalSq(vMean, vVariance);
    ASSERT_DOUBLE_EQ(uniNormalSq.mean()[0], 3);
    ASSERT_DOUBLE_EQ(uniNormalSq.covariance()[0], 1);
    ASSERT_EQ(uniNormalSq.dimension(), 4);
}


TEST(BivariateNormalDistributionSequence, vectorConstructor) {
    std::vector<double> vMean;
    vMean.push_back(3);
    vMean.push_back(4);
    std::vector<double> vVariance(4, 1);

    BivariateNormalDistributionSequence<double> bivariateNormalSeq(vMean, vVariance);
    ASSERT_EQ(bivariateNormalSeq.dimension(), 1);
}


TEST(UnivariateNormalDistributionSequence, eigenConstructor) {

    Eigen::Matrix<double, 4, 1> mean;
    mean << 3.0, 4.0, 5.0, 6.0;
    Eigen::Matrix<double, 4, 1> cov;
    cov << 1.0, 1.0, 1.0, 1.0;
    UnivariateNormalDistributionSequence<double> uniNormalSq(mean, cov);

    ASSERT_DOUBLE_EQ(uniNormalSq.mean()[0], 3);
    ASSERT_DOUBLE_EQ(uniNormalSq.covariance()[0], 1);
    ASSERT_EQ(uniNormalSq.dimension(), 4);
    // ASSERT_DOUBLE_EQ(4, uniNormal.upperBound(1.0)[0]);
    // ASSERT_DOUBLE_EQ(5, uniNormal.upperBound(1.0)[1]);
    // ASSERT_DOUBLE_EQ(2, uniNormal.lowerBound(1.0)[0]);
    // ASSERT_DOUBLE_EQ(2, uniNormal.lowerBound(2.0)[1]);
}

/*
TEST(UnivariateNormalDistributionArray, vectorConstructor) {
    std::vector<double> v_mean;
    v_mean.push_back(3);
    v_mean.push_back(4);
    v_mean.push_back(5);
    v_mean.push_back(6);
    std::vector<double> v_variance(4, 1);

    UnivariateNormalDistributionArray<double, 4> u_normal_dist_arr(v_mean, v_variance);

    ASSERT_DOUBLE_EQ(3, u_normal_dist_arr.mean()[0]);
    ASSERT_DOUBLE_EQ(1, u_normal_dist_arr.variance()[0]);
    ASSERT_DOUBLE_EQ(4, u_normal_dist_arr.dimension());
    ASSERT_DOUBLE_EQ(4, u_normal_dist_arr.upperBound(1.0)[0]);
    ASSERT_DOUBLE_EQ(5, u_normal_dist_arr.upperBound(1.0)[1]);
    ASSERT_DOUBLE_EQ(2, u_normal_dist_arr.lowerBound(1.0)[0]);
    ASSERT_DOUBLE_EQ(2, u_normal_dist_arr.lowerBound(2.0)[1]);
}


TEST(UnivariateNormalDistributionArray, upperSum) {
    std::vector<double> v_mean;
    v_mean.push_back(3);
    v_mean.push_back(4);
    v_mean.push_back(5);
    v_mean.push_back(6);
    std::vector<double> v_variance(4, 1);

    UnivariateNormalDistributionArray<double, 4> u_normal_dist_arr(v_mean, v_variance);

    Eigen::Matrix<double, 4, 1> m_mean = u_normal_dist_arr.mean();
    std::vector<double> v_mean_(m_mean.data(), m_mean.data() + m_mean.rows() * m_mean.cols());
    ASSERT_DOUBLE_EQ(18.0, std::accumulate(v_mean_.begin(), v_mean_.end(), 0.0));

    std::vector<double> v_up = u_normal_dist_arr.upperBound(1.0);
    ASSERT_DOUBLE_EQ(22.0, std::accumulate(v_up.begin(), v_up.end(), 0.0));

    std::vector<double> v_lw = u_normal_dist_arr.lowerBound(1.0);
    ASSERT_DOUBLE_EQ(14.0, std::accumulate(v_lw.begin(), v_lw.end(), 0.0));
}
*/

int main(int argc, char** argv) {
    ::google::InitGoogleLogging(argv[0]);
    ::google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_colorlogtostderr = true;
    FLAGS_logtostderr = true;

    return RUN_ALL_TESTS();
}
