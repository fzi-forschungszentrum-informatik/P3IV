#pragma once
#include <memory>
#include <vector>
#include <glog/logging.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include "p3iv_types/internal/point2d.hpp"

namespace py = pybind11;

namespace p3iv_types {
namespace python_converters {

template <typename T>
std::vector<T> numpyArray2Vector(const py::array_t<T>& arr) {
    // check dimensions first
    if (arr.ndim() != 1) {
        throw std::invalid_argument(
            (std::string("Number of dimension must be 1, but is ") + std::to_string(arr.ndim()) + std::string(".\n"))
                .c_str());
    }

    std::vector<T> vec;
    vec.reserve(arr.size());
    for (size_t i = 0; i < arr.size(); i++) {
        vec.emplace_back(arr.at(i));
    }
    auto v = std::move(vec); // workaround for RVO
    return v;
}

template <typename T>
py::array_t<T> vector2NumpyArray(const std::vector<T>& vec) {
    py::array_t<T> output(vec.size(), vec.data());
    return output;
}

internal::VectorPoint2d<double> numpyArray2VectorPoint2d(const py::array_t<double>& arr) {
    // check dimensions first
    if (arr.ndim() != 2) {
        throw std::invalid_argument(
            (std::string("Number of dimension must be 2, but is ") + std::to_string(arr.ndim()) + std::string(".\n"))
                .c_str());
    }
    if (arr.shape(1) != 2) {
        throw std::invalid_argument(
            (std::string("Number of columns must be 2, but is ") + std::to_string(arr.shape(1)) + std::string(".\n"))
                .c_str());
    }

    auto rawArray = arr.unchecked<2>();
    size_t numberOfPoints = rawArray.shape(0);

    std::vector<internal::Point2d<double>> vec;
    vec.reserve(numberOfPoints);
    for (size_t i = 0; i < numberOfPoints; i++) {
        vec.emplace_back(numpyArray2Point2d(rawArray));
    }

    internal::VectorPoint2d<double> v(vec);
    return v;
}

inline internal::Point2d<double> numpyArray2Point2d(const py::array_t<double>& pointarray) {
    internal::Point2d<double> p;
    p(0) = pointarray.at(0);
    p(1) = pointarray.at(1);
    return p;
}
} // namespace python_converters
} // namespace p3iv_types