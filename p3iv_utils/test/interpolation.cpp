#include "interpolation.hpp"
#include <chrono>
#include <iostream>
#include <vector>
#include <glog/logging.h>
#include "gtest/gtest.h"

using namespace p3iv_utils;


TEST(Interpolation, intervalOpen) {
    std::vector<double> x{0.0, 2.0, 4.0, 6.0, 8.0};
    std::vector<double> y{0.0, 4.0, 16.0, 36.0, 64.0};
    std::vector<double> x_intp{1.0, 3.0, 5.0, 7.0};

    auto y_intp = interpolate<double>(x, y, x_intp);

    for (size_t i = 0; i < x_intp.size(); i++) {
        ASSERT_DOUBLE_EQ(y_intp[i], x_intp[i] * x_intp[i]);
    }
}


TEST(Interpolation, intervalClosed) {
    std::vector<double> x{0.0, 2.0, 4.0, 6.0, 8.0};
    std::vector<double> y{0.0, 4.0, 16.0, 36.0, 64.0};
    std::vector<double> x_intp{0.0, 3.0, 8.0};

    auto y_intp = interpolate<double>(x, y, x_intp);

    for (size_t i = 0; i < x_intp.size(); i++) {
        ASSERT_DOUBLE_EQ(y_intp[i], x_intp[i] * x_intp[i]);
    }
}


TEST(Interpolation, intervalExtended) {
    std::vector<double> x{0.0, 2.0, 4.0, 6.0, 8.0};
    std::vector<double> y{0.0, 4.0, 16.0, 36.0, 64.0};
    std::vector<double> x_intp{0.0, 3.0, 9.0, 12.0};

    auto y_intp = interpolate<double>(x, y, x_intp);

    for (size_t i = 0; i < x_intp.size(); i++) {
        ASSERT_DOUBLE_EQ(y_intp[i], x_intp[i] * x_intp[i]);
    }
}


TEST(Interpolation, timeTnterval) {
    std::vector<double> y{0.0, 2.0, 4.0, 6.0};

    std::chrono::milliseconds t0(0);
    std::chrono::milliseconds t1(200);
    std::chrono::milliseconds t2(400);
    std::chrono::milliseconds t3(600);

    std::chrono::milliseconds t0_intp(100);
    std::chrono::milliseconds t1_intp(300);
    std::chrono::milliseconds t2_intp(500);

    std::vector<std::chrono::milliseconds> t{t0, t1, t2, t3};
    std::vector<std::chrono::milliseconds> t_intp{t0_intp, t1_intp, t2_intp};

    auto y_intp = interpolate<double>(t, y, t_intp);

    ASSERT_DOUBLE_EQ(y_intp[0], 1.0);
    ASSERT_DOUBLE_EQ(y_intp[1], 3.0);
    ASSERT_DOUBLE_EQ(y_intp[2], 5.0);
}