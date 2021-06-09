/*
 * This file is part of the Interpolated Polyline (https://github.com/...),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <cmath>
#include <iostream>
#include <sstream>
#include <glog/logging.h>
#include <gtest/gtest.h>
#include "interpolated_polyline.hpp"

using namespace interpolated_polyline;


TEST(InterpolatedPolyline, SignedDistance) {

    std::vector<double> line{-2.0, 1.0, 0.0, 1.0, 2.0, 1.0};
    InterpolatedPolyline interpolated_polyline(line);

    // test the distance at a MIDDLE-segment
    auto d_middle = interpolated_polyline.signedDistance(0.2, 2.0);
    ASSERT_DOUBLE_EQ(d_middle, 1.0);

    // test the distance at a line-to-line connection point
    auto d = interpolated_polyline.signedDistance(0.0, 2.0);
    ASSERT_DOUBLE_EQ(d, 1.0);

    // test the distance at the FIRST-segment
    auto d_first = interpolated_polyline.signedDistance(-4.0, -1.0);
    ASSERT_DOUBLE_EQ(d_first, -2.0 * pow(2, 0.5));

    // test the distance at the LAST-segment
    auto d_last = interpolated_polyline.signedDistance(4.0, 3.0);
    ASSERT_DOUBLE_EQ(d_last, 2.0 * pow(2, 0.5));
}


TEST(InterpolatedPolyline, Match) {

    std::vector<double> line{-2.0, 1.0, 0.0, 1.0, 2.0, 1.0};
    InterpolatedPolyline interpolated_polyline(line);

    auto match = interpolated_polyline.match(0.0, 2.0);
    ASSERT_DOUBLE_EQ(std::get<0>(match), 2.0); // arc_length
    ASSERT_DOUBLE_EQ(std::get<1>(match), 1.0); // normal_distance
}


TEST(InterpolatedPolyline, Reconstruct) {

    std::vector<double> line{-2.0, 1.0, 0.0, 1.0, 2.0, 1.0};
    InterpolatedPolyline interpolated_distance(line);

    auto reconstruct = interpolated_distance.reconstruct(2.0, 1.0);
    ASSERT_DOUBLE_EQ(std::get<0>(reconstruct), 0.0); // arc_length
    ASSERT_DOUBLE_EQ(std::get<1>(reconstruct), 2.0); // normal_distance
}


TEST(InterpolatedPolyline, Arclengths) {

    std::vector<double> line{-2.0, 0.0, 0.0, 1.5, 2.0, 3.0};
    InterpolatedPolyline interpolated_polyline(line);
    auto length = interpolated_polyline.maxArclength();
    ASSERT_DOUBLE_EQ(length, 5.0); // arc_length
}


TEST(InterpolatedPolyline, Tangent) {

    std::vector<double> line{0.0, 0.0, 3.0, 4.0, 6.0, 8.0, 9.0, 12.0};
    InterpolatedPolyline interpolated_polyline(line);
    auto dTangent = interpolated_polyline.tangent(5., 5.);
    auto tan = std::get<1>(dTangent);
    ASSERT_DOUBLE_EQ(tan, atan2(4, 3));
}


TEST(InterpolatedPolyline, InterpTangent) {

    std::vector<double> line{0.0, 0.0, 2.0, 2.0, 4.0, 2.0, 6.0, 4.0, 8.0, 4.0};
    InterpolatedPolyline interpolated_polyline(line);

    ASSERT_NEAR(std::get<1>(interpolated_polyline.tangent(3.0, 2.5)), 0.463648, 1e-3); ///< ~26.57 degrees
    ASSERT_NEAR(std::get<1>(interpolated_polyline.tangent(5.0, 3.0)), 0.785398, 1e-3); ///< ~45.00 degrees
    ASSERT_NEAR(std::get<1>(interpolated_polyline.tangent(6.0, 5.0)), 0.380506, 1e-3); ///< ~21.80 degrees
    ASSERT_NEAR(std::get<1>(interpolated_polyline.tangent(7.0, 4.0)), 0.25, 1e-3);     ///< ~14.32 degrees
    ASSERT_NEAR(std::get<1>(interpolated_polyline.tangent(7.0, 4.1)), 0.239232, 1e-3); ///< ~13.71 degrees
    ASSERT_NEAR(std::get<1>(interpolated_polyline.tangent(8.0, 4.0)), 0.5, 1e-3);      ///< ~28.65 degrees
    /// P.S. atan(1/2) ~= 26.57 degrees
}


int main(int argc, char** argv) {
    google::InitGoogleLogging(argv[0]);
    google::InstallFailureSignalHandler();
    FLAGS_v = 2;
    FLAGS_stderrthreshold = 0;
    FLAGS_colorlogtostderr = true;
    FLAGS_alsologtostderr = false;
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
