#include <algorithm>
#include <map>
#include <vector>
#include <glog/logging.h>
#include <gtest/gtest.h>
#include "p3iv_types/traffic_rules.hpp"

namespace p3iv_types {


TEST(TypesCPP, Stopline) {
    Stopline stop(10, true);
}


TEST(TypesCPP, Speedlimit) {
    Speedlimit speedlimit(13.89, 45.0);
}


TEST(TypesCPP, TrafficRules) {
    TrafficRules t;

    Stopline stop(10, true);
    t.addStopline(stop);

    std::vector<double> distanceToStoplines{30.0, 50.0};
    std::vector<bool> hasToStops{false, true};
    t.addStopline(distanceToStoplines, hasToStops);

    Speedlimit speedlimit(13.89, 45.0);
    t.addSpeedlimit(speedlimit);
}


int main(int argc, char** argv) {
    google::InitGoogleLogging(argv[0]); // NOLINT
    google::InstallFailureSignalHandler();
    ::testing::InitGoogleTest(&argc, argv);

    FLAGS_v = 2;
    FLAGS_stderrthreshold = 0;
    FLAGS_colorlogtostderr = true;
    FLAGS_alsologtostderr = false;

    return RUN_ALL_TESTS();
}
} // namespace p3iv_types
