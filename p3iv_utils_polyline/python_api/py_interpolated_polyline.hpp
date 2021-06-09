/*
 * This file is part of the Interpolated Polyline (https://github.com/...),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include <iostream>
#include <memory>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include "interpolated_polyline.hpp"

namespace py = pybind11;
using NumpyArray = py::array_t<double>;


namespace interpolated_polyline {

class PyInterpolatedPolyline {
public:
    PyInterpolatedPolyline(const NumpyArray& xs, const NumpyArray& ys);

    /// returns distance
    double signedDistance(double x, double y);

    /// returns distance, tangent
    std::tuple<double, double> tangent(double x, double y);

    /// returns arclength, offset
    std::tuple<double, double> match(double x, double y);

    /// returns arclength, offset, tangent
    std::tuple<double, double, double> orientedMatch(double x, double y);

    /// returns reconstructed x, y
    std::tuple<double, double> reconstruct(double l, double d);

    /// returns maximum arclength
    double max_arclength();

private:
    std::unique_ptr<InterpolatedPolyline> polyline_ = nullptr;
};
} // namespace interpolated_polyline