#include <glog/logging.h>
#include <boost/math/distributions/lognormal.hpp>
#include <boost/math/special_functions/erf.hpp> // for erf/erfc.
#include "gtest/gtest.h"
#include "internal/approximations.hpp"

using namespace util_probability;


TEST(UtilNumeric, CDF) {

    double stddev = 1.0;
    double mean = 0.0;
    double sigma = 1.0;

    boost::math::normal norm(mean, stddev);

    double sigma_1_region = boost::math::cdf(norm, sigma) - boost::math::cdf(norm, -sigma);
    LOG_ASSERT(std::abs(sigma_1_region - 0.68) < 0.01);
    LOG_ASSERT(0.5 * boost::math::erfc(-sigma * M_SQRT1_2) == boost::math::cdf(norm, 1.0));

    double val = 0.5;
    auto boost_cdf = boost::math::cdf(norm, val);
    auto numeric_cdf = util_probability::norm_cdf(val, mean, sigma);
    LOG_ASSERT(std::abs(boost_cdf - numeric_cdf) < 1e-5);
}


int main(int argc, char** argv) {
    ::google::InitGoogleLogging(argv[0]);
    ::google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_colorlogtostderr = true;
    FLAGS_logtostderr = true;

    return RUN_ALL_TESTS();
}
