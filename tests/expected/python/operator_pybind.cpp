

#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.


#include "wrap/serialization.h"
#include <boost/serialization/export.hpp>





using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(operator_py, m_) {
    m_.doc() = "pybind11 wrapper of operator_py";


    py::class_<Pose3, std::shared_ptr<Pose3>>(m_, "Pose3")
        .def(py::init<>())
        .def(py::self * py::self);


#include "python/specializations.h"

}

