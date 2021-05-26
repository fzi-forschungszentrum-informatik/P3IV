#include <algorithm>
#include <map>
#include <vector>
#include <glog/logging.h>
#include <gtest/gtest.h>
#include "p3iv_types/motion_state.hpp"

namespace p3iv_types {

TEST(TypesCPP, MotionState) { // NOLINT
    MotionState m{};
    m.position.setMean(6.0, 8.0);
    m.position.setCovariance(9.0, 0.0, 0.0, 16.0);
    m.yaw.setMean(0.0);
    m.yaw.setCovariance(10.0);
    m.velocity.setMean(12.0, 16.0);
    m.velocity.setCovariance(0.0, 0.0, 0.0, 0.0);

    LOG(INFO) << "Motion state initialized.";
}

TEST(TypesCPP, MotionStateArray) { // NOLINT
    MotionStateArray<3> m{};
    std::vector<double> posMean(6, 2.0);
    std::vector<double> posCovariance(12, 0.0);
    std::vector<double> yawMean(3, 0.0);
    std::vector<double> yawCovariance(3, 0.0);

    m.position.setMean(posMean);
    m.position.setCovariance(posCovariance);

    m.yaw.setMean(yawMean);
    m.yaw.setCovariance(yawCovariance);

    // leave velocity with default values
    LOG(INFO) << "MotionStateArray initialized.";
}


int main(int argc, char** argv) {
    google::InitGoogleLogging(argv[0]); // NOLINT
    google::InstallFailureSignalHandler();
    FLAGS_v = 2;
    FLAGS_stderrthreshold = 0;
    FLAGS_colorlogtostderr = true;
    FLAGS_alsologtostderr = false;
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
} // namespace p3iv_types