/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <algorithm>
#include <map>
#include <vector>
#include <glog/logging.h>
#include <gtest/gtest.h>
#include "p3iv_types/visibility_information.hpp"

namespace p3iv_types {


TEST(TypesCPP, VisibilityInformation) {
    VisibilityInformation v(10.0, 30.0);
}


TEST(TypesCPP, Visibility) {
    Visibility v;
    std::vector<double> distances{20.0, 25.0, 30.0};
    std::vector<double> visibilityOfIntersections{10.0, 15.0, 0.0};
    v.setVisibility(distances, visibilityOfIntersections);

    VisibilityInformation vi = v.getVisibility(1);
    ASSERT_EQ(vi.distance, 25.0);
    ASSERT_EQ(vi.visibilityOfIntersection, 15.0);
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
