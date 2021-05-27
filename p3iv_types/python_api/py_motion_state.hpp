#pragma once
#include <pybind11/pybind11.h>
#include "motion_state.hpp"
#include "pybind_utils.hpp"

namespace py = pybind11;
using PyArray = py::array_t<double>;

namespace p3iv_types {

using namespace pybind_utils;

struct PyMotionState : MotionState {

    void setPosition(PyArray mean, PyArray covariance) {
        std::vector<double> m = pyArray2Vector<double>(mean);
        std::vector<double> c = pyArray2Vector<double>(covariance);
        this->position.setMean(m[0], m[1]);
        this->position.setCovariance(c[0], c[1], c[2], c[3]);
    }

    void setYaw(PyArray mean, PyArray covariance) {
        std::vector<double> m = pyArray2Vector<double>(mean);
        std::vector<double> c = pyArray2Vector<double>(covariance);
        this->yaw.setMean(m[0]);
        this->yaw.setCovariance(c[0]);
    }

    void setVelocity(PyArray mean, PyArray covariance) {
        std::vector<double> m = pyArray2Vector<double>(mean);
        std::vector<double> c = pyArray2Vector<double>(covariance);
        this->velocity.setMean(m[0], m[1]);
        this->velocity.setCovariance(c[0], c[1], c[2], c[3]);
    }
};


struct PyMotionStateArray : MotionStateArray {

    void setPosition(PyArray mean, PyArray covariance) {
        std::vector<double> m = pyArray2Vector<double>(mean);
        std::vector<double> c = pyArray2Vector<double>(covariance);
        this->position.setMean(m);
        this->position.setCovariance(c);
    }

    void setYaw(PyArray mean, PyArray covariance) {
        std::vector<double> m = pyArray2Vector<double>(mean);
        std::vector<double> c = pyArray2Vector<double>(covariance);
        this->yaw.setMean(m);
        this->yaw.setCovariance(c);
    }

    void setVelocity(PyArray mean, PyArray covariance) {
        std::vector<double> m = pyArray2Vector<double>(mean);
        std::vector<double> c = pyArray2Vector<double>(covariance);
        this->velocity.setMean(m);
        this->velocity.setCovariance(c);
    }
};

} // namespace p3iv_types