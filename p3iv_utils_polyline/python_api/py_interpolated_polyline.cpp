/*
 * This file is part of the Interpolated Polyline (https://github.com/...),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include "py_interpolated_polyline.hpp"
#include <iostream>
#include <memory>
#include <vector>


namespace py = pybind11;
using namespace interpolated_polyline;


std::vector<double> numpyArray2Vector(const NumpyArray& arr) {
    if (arr.ndim() != 1) {
        throw std::invalid_argument(
            (std::string("Number of dimension must be 1, but is ") + std::to_string(arr.ndim()) + std::string(".\n"))
                .c_str());
    }

    std::vector<double> vec;
    vec.reserve(arr.size());
    for (size_t i = 0; i < arr.size(); i++) {
        vec.emplace_back(arr.at(i));
    }

    return vec;
}


PyInterpolatedPolyline::PyInterpolatedPolyline(const NumpyArray& xs_np, const NumpyArray& ys_np) {
    std::vector<double> xs = numpyArray2Vector(xs_np);
    std::vector<double> ys = numpyArray2Vector(ys_np);
    polyline_ = std::unique_ptr<InterpolatedPolyline>(new InterpolatedPolyline(xs, ys));
}

double PyInterpolatedPolyline::signedDistance(double x, double y) {
    return polyline_->signedDistance(x, y);
}

std::tuple<double, double> PyInterpolatedPolyline::tangent(double x, double y) {
    auto sign = polyline_->tangent(x, y);
    double d = std::get<0>(sign);
    double tangent = std::get<1>(sign);
    return std::make_tuple(d, tangent);
}

std::tuple<double, double> PyInterpolatedPolyline::match(double x, double y) {
    auto match = polyline_->match(x, y);
    double l = std::get<0>(match);
    double d = std::get<1>(match);
    return std::make_tuple(l, d);
}

std::tuple<double, double, double> PyInterpolatedPolyline::orientedMatch(double x, double y) {
    auto orientedMatch = polyline_->orientedMatch(x, y);
    double l = std::get<0>(orientedMatch);
    double d = std::get<1>(orientedMatch);
    double t = std::get<2>(orientedMatch);
    return std::make_tuple(l, d, t);
}

std::tuple<double, double> PyInterpolatedPolyline::reconstruct(double arclen, double offset) {
    auto reconstruct = polyline_->reconstruct(arclen, offset);
    double x = std::get<0>(reconstruct);
    double y = std::get<1>(reconstruct);
    return std::make_tuple(x, y);
}

double PyInterpolatedPolyline::max_arclength() {
    return polyline_->maxArclength();
}


PYBIND11_MODULE(PYTHON_API_MODULE_NAME, m) {
    m.doc() = R"pbdoc(
                Pybind11 bindings of interpolated polyline
                -----------------------
                .. currentmodule:: PYTHON_API_MODULE_NAME
                .. autosummary::
                   :toctree: _generate

            )pbdoc";

    py::class_<PyInterpolatedPolyline>(m, "PyInterpolatedPolyline", py::module_local())
        .def(py::init<const NumpyArray&, const NumpyArray&>())
        .def("signed_distance", &PyInterpolatedPolyline::signedDistance)
        .def("tangent", &PyInterpolatedPolyline::tangent)
        .def("match", &PyInterpolatedPolyline::match)
        .def("oriented_match", &PyInterpolatedPolyline::orientedMatch)
        .def("reconstruct", &PyInterpolatedPolyline::reconstruct)
        .def("max_arclength", &PyInterpolatedPolyline::max_arclength);


#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
