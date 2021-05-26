#pragma once
#include <vector>
#include "internal/point2d.hpp"


namespace p3iv_types {

using Point2d = internal::Point2d<double>;
using VectorPoint2d = internal::VectorPoint2d<double>;


struct DrivingCorridor {

    DrivingCorridor() = default;

    DrivingCorridor(const VectorPoint2d& r, const VectorPoint2d& c, const VectorPoint2d& l)
            : right{r}, center{c}, left{l} {};

    VectorPoint2d right;
    VectorPoint2d center;
    VectorPoint2d left;
};
} // namespace p3iv_types