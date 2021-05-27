#include "py_motion_state.hpp"
#include <iostream>
#include <memory>
#include <glog/logging.h>
#include <pybind11/pybind11.h>

using namespace p3iv_types;
namespace py = pybind11;


// The module name here *must* match the name of the python project. You can use the PYTHON_API_MODULE_NAME definition.
PYBIND11_MODULE(PYTHON_API_MODULE_NAME, m) {
    m.doc() = R"pbdoc(
            Python bindings for C++ Implementation
            -----------------------
            .. currentmodule:: PYTHON_API_MODULE_NAME
            .. autosummary::
               :toctree: _generate

        )pbdoc";

    py::class_<PyMotionState>(m, "PyMotionState", py::module_local())
        .def(py::init<>())
        .def("setPosition", &PyMotionState::setPosition, py::arg("mean"), py::arg("covariance"))
        .def("setYaw", &PyMotionState::setYaw, py::arg("mean"), py::arg("covariance"))
        .def("setVelocity", &PyMotionState::setVelocity, py::arg("mean"), py::arg("covariance"));

    py::class_<PyMotionStateArray>(m, "PyMotionStateArray", py::module_local())
        .def(py::init<>())
        .def("setPosition", &PyMotionStateArray::setPosition, py::arg("mean"), py::arg("covariance"))
        .def("setYaw", &PyMotionStateArray::setYaw, py::arg("mean"), py::arg("covariance"))
        .def("setVelocity", &PyMotionStateArray::setVelocity, py::arg("mean"), py::arg("covariance"));


#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
