#include <algorithm>
#include <map>
#include <vector>
#include <glog/logging.h>
#include <gtest/gtest.h>
#include "p3iv_types/tracked_object.hpp"

namespace p3iv_types {

TEST(TypesCPP, TrackedObject) { // NOLINT
    TrackedObject t(10);
}

TEST(TypesCPP, TrackedVehicle) { // NOLINT
    TrackedVehicle t(10, 2.7, 3.5);
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