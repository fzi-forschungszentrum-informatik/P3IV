// google test docs
// wiki page: https://code.google.com/p/googletest/w/list
// primer: https://code.google.com/p/googletest/wiki/V1_7_Primer
// FAQ: https://code.google.com/p/googletest/wiki/FAQ
// advanced guide: https://code.google.com/p/googletest/wiki/V1_7_AdvancedGuide
// samples: https://code.google.com/p/googletest/wiki/V1_7_Samples
//
// List of some basic tests functions:
// Fatal assertion                      Nonfatal assertion Verifies /
// Description
//-------------------------------------------------------------------------------------------------------------------------------------------------------
// ASSERT_EQ(expected, actual);         EXPECT_EQ(expected, actual); expected ==
// actual ASSERT_NE(val1, val2);               EXPECT_NE(val1, val2); val1 !=
// val2 ASSERT_LT(val1, val2);               EXPECT_LT(val1, val2); val1 < val2
// ASSERT_LE(val1, val2);               EXPECT_LE(val1, val2); val1 <= val2
// ASSERT_GT(val1, val2);               EXPECT_GT(val1, val2); val1 > val2
// ASSERT_GE(val1, val2);               EXPECT_GE(val1, val2); val1 >= val2
//
// ASSERT_FLOAT_EQ(expected, actual);   EXPECT_FLOAT_EQ(expected, actual);   the
// two float values are almost equal (4 ULPs) ASSERT_DOUBLE_EQ(expected,
// actual); EXPECT_DOUBLE_EQ(expected, actual);  the two double values are
// almost equal (4 ULPs) ASSERT_NEAR(val1, val2, abs_error);  EXPECT_NEAR(val1,
// val2, abs_error); the difference between val1 and val2 doesn't exceed the
// given absolute error
//
// Note: more information about ULPs can be found here:
// http://www.cygnus-software.com/papers/comparingfloats/comparingfloats.htm
//
// Example of two unit test:
// TEST(Math, Add) {
//    ASSERT_EQ(10, 5+ 5);
//}
//
// TEST(Math, Float) {
//	  ASSERT_FLOAT_EQ((10.0f + 2.0f) * 3.0f, 10.0f * 3.0f + 2.0f * 3.0f)
//}
//=======================================================================================================================================================
#include "kinematics.hpp"
#include "gtest/gtest.h"

using namespace p3iv_utils;


TEST(Kinematics, constructEmpty) {
    Kinematics<double> kinematics;
}


TEST(Kinematics, constructWheelbase) {
    Kinematics<double> kinematics(2.7);
}


TEST(Kinematics, callMethods) {
    Kinematics<double> kinematics(2.7);
    ASSERT_LE(kinematics.turnCurvature(8.0, 6.0, 2.0, 1.5) - 0.0040, 1e-3);
    ASSERT_LE(kinematics.yawAngle(8.0, 6.0) - 0.6435, 1e-3);
    ASSERT_LE(kinematics.steeringAngle(8.0, 6.0, 2.0, 1.5) - 0.0108, 1e-3);
    ASSERT_LE(kinematics.speed(8.0, 6.0) - 10.0, 1e-3);
    ASSERT_LE(kinematics.acceleration(2.0, 1.5) - 2.8284, 1e-3);
    ASSERT_LE(kinematics.centripetalAcceleration(8.0, 6.0, 2.0, 1.5) - 0.4, 1e-3);
}
