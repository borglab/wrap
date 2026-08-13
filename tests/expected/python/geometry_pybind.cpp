#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.

#include "gtsam/geometry/Point2.h"
#include "gtsam/geometry/Point3.h"
#include <boost/serialization/export.hpp>
#include <type_traits>

namespace gtwrap {
namespace internal {

template <typename T>
struct PyArgPolicy {
  static pybind11::arg make(const char* name) { return pybind11::arg(name); }
};

template <typename T>
pybind11::arg py_arg(const char* name) {
  return PyArgPolicy<typename std::decay<T>::type>::make(name);
}

}  // namespace internal
}  // namespace gtwrap

namespace gtwrap {
namespace internal {

template <typename... Args>
struct SelectOverload {
  template <typename Return>
  static constexpr auto function(Return (*pointer)(Args...))
      -> decltype(pointer) {
    return pointer;
  }

  template <typename Return, typename Class>
  static constexpr auto method(Return (Class::*pointer)(Args...))
      -> decltype(pointer) {
    return pointer;
  }

  template <typename Return, typename Class>
  static constexpr auto const_method(Return (Class::*pointer)(Args...) const)
      -> decltype(pointer) {
    return pointer;
  }
};

}  // namespace internal
}  // namespace gtwrap


BOOST_CLASS_EXPORT(gtsam::Point2)
BOOST_CLASS_EXPORT(gtsam::Point3)


using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(geometry_py, m_) {
    m_.doc() = "pybind11 wrapper of geometry_py";

    pybind11::module m_gtsam = m_.def_submodule("gtsam", "gtsam submodule");

    py::class_<gtsam::Point2, std::shared_ptr<gtsam::Point2>>(m_gtsam, "Point2")
        .def(py::init<>())
        .def(py::init<double, double>(), gtwrap::internal::py_arg<double>("x"), gtwrap::internal::py_arg<double>("y"))
        .def("x",gtwrap::internal::SelectOverload<>::const_method(&gtsam::Point2::x))
        .def("y",gtwrap::internal::SelectOverload<>::const_method(&gtsam::Point2::y))
        .def("dim",gtwrap::internal::SelectOverload<>::const_method(&gtsam::Point2::dim))
        .def("returnChar",gtwrap::internal::SelectOverload<>::const_method(&gtsam::Point2::returnChar))
        .def("argChar",gtwrap::internal::SelectOverload<char>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<char>("a"))
        .def("argChar",gtwrap::internal::SelectOverload<std::shared_ptr<char>>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<std::shared_ptr<char>>("a"))
        .def("argChar",gtwrap::internal::SelectOverload<char&>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<char&>("a"))
        .def("argChar",gtwrap::internal::SelectOverload<char*>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<char*>("a"))
        .def("argChar",gtwrap::internal::SelectOverload<const std::shared_ptr<char>>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<const std::shared_ptr<char>>("a"))
        .def("argChar",gtwrap::internal::SelectOverload<const char&>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<const char&>("a"))
        .def("argChar",gtwrap::internal::SelectOverload<const char*>::const_method(&gtsam::Point2::argChar), gtwrap::internal::py_arg<const char*>("a"))
        .def("argUChar",gtwrap::internal::SelectOverload<unsigned char>::const_method(&gtsam::Point2::argUChar), gtwrap::internal::py_arg<unsigned char>("a"))
        .def("eigenArguments",gtwrap::internal::SelectOverload<const gtsam::Vector&, const gtsam::Matrix&>::const_method(&gtsam::Point2::eigenArguments), gtwrap::internal::py_arg<const gtsam::Vector&>("v"), gtwrap::internal::py_arg<const gtsam::Matrix&>("m"))
        .def("vectorConfusion",gtwrap::internal::SelectOverload<>::method(&gtsam::Point2::vectorConfusion))
        .def("serialize", [](gtsam::Point2* self){ return gtsam::serialize(*self); })
        .def("deserialize", [](gtsam::Point2* self, string serialized){ gtsam::deserialize(serialized, *self); }, py::arg("serialized"))
        .def(py::pickle(
            [](const gtsam::Point2 &a){ /* __getstate__: Returns a string that encodes the state of the object */ return py::make_tuple(gtsam::serialize(a)); },
            [](py::tuple t){ /* __setstate__ */ gtsam::Point2 obj; gtsam::deserialize(t[0].cast<std::string>(), obj); return obj; }));

    py::class_<gtsam::Point3, std::shared_ptr<gtsam::Point3>>(m_gtsam, "Point3")
        .def(py::init<double, double, double>(), gtwrap::internal::py_arg<double>("x"), gtwrap::internal::py_arg<double>("y"), gtwrap::internal::py_arg<double>("z"))
        .def("norm",gtwrap::internal::SelectOverload<>::const_method(&gtsam::Point3::norm))
        .def("serialize", [](gtsam::Point3* self){ return gtsam::serialize(*self); })
        .def("deserialize", [](gtsam::Point3* self, string serialized){ gtsam::deserialize(serialized, *self); }, py::arg("serialized"))
        .def(py::pickle(
            [](const gtsam::Point3 &a){ /* __getstate__: Returns a string that encodes the state of the object */ return py::make_tuple(gtsam::serialize(a)); },
            [](py::tuple t){ /* __setstate__ */ gtsam::Point3 obj; gtsam::deserialize(t[0].cast<std::string>(), obj); return obj; }))
        .def_static("staticFunction",gtwrap::internal::SelectOverload<>::function(&gtsam::Point3::staticFunction))
        .def_static("StaticFunctionRet",gtwrap::internal::SelectOverload<double>::function(&gtsam::Point3::StaticFunctionRet), gtwrap::internal::py_arg<double>("z"));


#include "python/specializations.h"

}

