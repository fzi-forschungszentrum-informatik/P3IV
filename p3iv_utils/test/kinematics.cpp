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
