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
#include "finite_differences.hpp"
#include "gtest/gtest.h"

using namespace p3iv_utils;


TEST(FiniteDifferences, testValueDifferences) {
    double dt = 1.0;
    std::vector<double> x{10.0, 12.0, 15.0, 20.0};

    std::vector<double> v;
    for (size_t i = 1; i < x.size(); i++) {
        double vi = derive_1(dt, x[i - 1], x[i]);
        v.push_back(vi);
    }

    std::vector<double> a;
    for (size_t i = 2; i < x.size(); i++) {
        double ai = derive_2(dt, x[i - 2], x[i - 1], x[i]);
        a.push_back(ai);
    }

    std::vector<double> j;
    for (size_t i = 3; i < x.size(); i++) {
        double ji = derive_3(dt, x[i - 3], x[i - 2], x[i - 1], x[i]);
        j.push_back(ji);
    }

    ASSERT_DOUBLE_EQ(v[0], 2.0);
    ASSERT_DOUBLE_EQ(v[1], 3.0);
    ASSERT_DOUBLE_EQ(v[2], 5.0);

    ASSERT_DOUBLE_EQ(a[0], 1.0);
    ASSERT_DOUBLE_EQ(a[1], 2.0);

    ASSERT_DOUBLE_EQ(j[0], 1.0);
}


TEST(FiniteDifferences, testPtrDifferences) {
    double dt = 1.0;

    double x0 = 10.0;
    double x1 = 12.0;
    double x2 = 15.0;
    double x3 = 20.0;

    double* px0 = &x0;
    double* px1 = &x1;
    double* px2 = &x2;
    double* px3 = &x3;
    std::vector<double*> x{px0, px1, px2, px3};

    std::vector<double> v;
    for (size_t i = 1; i < x.size(); i++) {
        double vi = derive_1(dt, x[i - 1], x[i]);
        v.push_back(vi);
    }

    std::vector<double> a;
    for (size_t i = 2; i < x.size(); i++) {
        double ai = derive_2(dt, x[i - 2], x[i - 1], x[i]);
        a.push_back(ai);
    }

    std::vector<double> j;
    for (size_t i = 3; i < x.size(); i++) {
        double ji = derive_3(dt, x[i - 3], x[i - 2], x[i - 1], x[i]);
        j.push_back(ji);
    }

    ASSERT_DOUBLE_EQ(v[0], 2.0);
    ASSERT_DOUBLE_EQ(v[1], 3.0);
    ASSERT_DOUBLE_EQ(v[2], 5.0);

    ASSERT_DOUBLE_EQ(a[0], 1.0);
    ASSERT_DOUBLE_EQ(a[1], 2.0);

    ASSERT_DOUBLE_EQ(j[0], 1.0);
}