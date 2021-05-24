// google test docs
// wiki page: https://code.google.com/p/googletest/w/list
// primer: https://code.google.com/p/googletest/wiki/V1_7_Primer
// FAQ: https://code.google.com/p/googletest/wiki/FAQ
// advanced guide: https://code.google.com/p/googletest/wiki/V1_7_AdvancedGuide
// samples: https://code.google.com/p/googletest/wiki/V1_7_Samples
//
#include <glog/logging.h>
#include <gtest/gtest.h>

#include <algorithm>
#include <map>
#include <vector>
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

} // namespace p3iv_types

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