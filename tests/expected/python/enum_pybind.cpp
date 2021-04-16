

#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.


#include "wrap/serialization.h"
#include <boost/serialization/export.hpp>





using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(enum_py, m_) {
    m_.doc() = "pybind11 wrapper of enum_py";

py::enum_<Kind>(m_, "Kind", py::arithmetic())
        .value("Dog", Kind::Dog)
        .value("Cat", Kind::Cat)
        .export_values();

#include "python/specializations.h"

}

