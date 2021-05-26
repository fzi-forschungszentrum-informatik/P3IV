#include <algorithm>
#include <map>
#include <vector>
#include <glog/logging.h>
#include <gtest/gtest.h>
#include "p3iv_types/route_option.hpp"

namespace p3iv_types {


TEST(TypesCPP, RouteOptionEmpty) {
    RouteOption r;
}


TEST(TypesCPP, RouteOptionSetEmpty) {
    RouteOption r;
    DrivingCorridor d;
    r.setDrivingCorridor(d);
}


TEST(TypesCPP, DrivingCorridor) {
    std::vector<double> vx(6, 0.0);
    std::vector<double> vy{0.0, 1.0, 2.0, 3.0, 4.0, 5.0};
    VectorPoint2d vp(vx, vy);
    DrivingCorridor d(vp, vp, vp);
}


TEST(TypesCPP, RouteOptionSetCorridor) {
    RouteOption r;
    std::vector<double> vx(6, 0.0);
    std::vector<double> vy{0.0, 1.0, 2.0, 3.0, 4.0, 5.0};
    VectorPoint2d vp(vx, vy);
    DrivingCorridor d(vp, vp, vp);
    r.setDrivingCorridor(d);
}


TEST(TypesCPP, RouteOptionCtor) {
    std::vector<double> vx(6, 0.0);
    std::vector<double> vy{0.0, 1.0, 2.0, 3.0, 4.0, 5.0};
    VectorPoint2d vp(vx, vy);
    DrivingCorridor d(vp, vp, vp);
    RouteOption r(d);
}


TEST(TypesCPP, RouteOptionCtorVector) {
    std::vector<double> vx(6, 0.0);
    std::vector<double> vy{0.0, 1.0, 2.0, 3.0, 4.0, 5.0};
    VectorPoint2d vp(vx, vy);
    RouteOption r(vp, vp, vp);
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
