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


BOOST_CLASS_EXPORT(gtsam::Point2)
BOOST_CLASS_EXPORT(gtsam::Point3)


using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(geometry_py, m_) {
    m_.doc() = "pybind11 wrapper of geometry_py";


    // Named adapters avoid a unique callable type per binding.
    struct gtwrap_generated_adapters {
        static auto callable_0(gtsam::Point2* self) -> std::decay<decltype(self->x())>::type { return self->x(); }
        static auto callable_1(gtsam::Point2* self) -> std::decay<decltype(self->y())>::type { return self->y(); }
        static auto callable_2(gtsam::Point2* self) -> std::decay<decltype(self->dim())>::type { return self->dim(); }
        static auto callable_3(gtsam::Point2* self) -> std::decay<decltype(self->returnChar())>::type { return self->returnChar(); }
        static void callable_4(gtsam::Point2* self, char a) { self->argChar(a); }
        static void callable_5(gtsam::Point2* self, std::shared_ptr<char> a) { self->argChar(a); }
        static void callable_6(gtsam::Point2* self, char& a) { self->argChar(a); }
        static void callable_7(gtsam::Point2* self, char* a) { self->argChar(a); }
        static void callable_8(gtsam::Point2* self, const std::shared_ptr<char> a) { self->argChar(a); }
        static void callable_9(gtsam::Point2* self, const char& a) { self->argChar(a); }
        static void callable_10(gtsam::Point2* self, const char* a) { self->argChar(a); }
        static void callable_11(gtsam::Point2* self, unsigned char a) { self->argUChar(a); }
        static void callable_12(gtsam::Point2* self, const gtsam::Vector& v, const gtsam::Matrix& m) { self->eigenArguments(v, m); }
        static auto callable_13(gtsam::Point2* self) -> std::decay<decltype(self->vectorConfusion())>::type { return self->vectorConfusion(); }
        static auto callable_14(gtsam::Point3* self) -> std::decay<decltype(self->norm())>::type { return self->norm(); }
        static auto callable_15() -> std::decay<decltype(gtsam::Point3::staticFunction())>::type { return gtsam::Point3::staticFunction(); }
        static auto callable_16(double z) -> std::decay<decltype(gtsam::Point3::StaticFunctionRet(z))>::type { return gtsam::Point3::StaticFunctionRet(z); }
    };
    pybind11::module m_gtsam = m_.def_submodule("gtsam", "gtsam submodule");

    py::class_<gtsam::Point2, std::shared_ptr<gtsam::Point2>>(m_gtsam, "Point2")
        .def(py::init<>())
        .def(py::init<double, double>(), gtwrap::internal::py_arg<double>("x"), gtwrap::internal::py_arg<double>("y"))
        .def("x",&gtwrap_generated_adapters::callable_0)
        .def("y",&gtwrap_generated_adapters::callable_1)
        .def("dim",&gtwrap_generated_adapters::callable_2)
        .def("returnChar",&gtwrap_generated_adapters::callable_3)
        .def("argChar",&gtwrap_generated_adapters::callable_4, gtwrap::internal::py_arg<char>("a"))
        .def("argChar",&gtwrap_generated_adapters::callable_5, gtwrap::internal::py_arg<std::shared_ptr<char>>("a"))
        .def("argChar",&gtwrap_generated_adapters::callable_6, gtwrap::internal::py_arg<char&>("a"))
        .def("argChar",&gtwrap_generated_adapters::callable_7, gtwrap::internal::py_arg<char*>("a"))
        .def("argChar",&gtwrap_generated_adapters::callable_8, gtwrap::internal::py_arg<const std::shared_ptr<char>>("a"))
        .def("argChar",&gtwrap_generated_adapters::callable_9, gtwrap::internal::py_arg<const char&>("a"))
        .def("argChar",&gtwrap_generated_adapters::callable_10, gtwrap::internal::py_arg<const char*>("a"))
        .def("argUChar",&gtwrap_generated_adapters::callable_11, gtwrap::internal::py_arg<unsigned char>("a"))
        .def("eigenArguments",&gtwrap_generated_adapters::callable_12, gtwrap::internal::py_arg<const gtsam::Vector&>("v"), gtwrap::internal::py_arg<const gtsam::Matrix&>("m"))
        .def("vectorConfusion",&gtwrap_generated_adapters::callable_13)
        .def("serialize", [](gtsam::Point2* self){ return gtsam::serialize(*self); })
        .def("deserialize", [](gtsam::Point2* self, string serialized){ gtsam::deserialize(serialized, *self); }, py::arg("serialized"))
        .def(py::pickle(
            [](const gtsam::Point2 &a){ /* __getstate__: Returns a string that encodes the state of the object */ return py::make_tuple(gtsam::serialize(a)); },
            [](py::tuple t){ /* __setstate__ */ gtsam::Point2 obj; gtsam::deserialize(t[0].cast<std::string>(), obj); return obj; }));

    py::class_<gtsam::Point3, std::shared_ptr<gtsam::Point3>>(m_gtsam, "Point3")
        .def(py::init<double, double, double>(), gtwrap::internal::py_arg<double>("x"), gtwrap::internal::py_arg<double>("y"), gtwrap::internal::py_arg<double>("z"))
        .def("norm",&gtwrap_generated_adapters::callable_14)
        .def("serialize", [](gtsam::Point3* self){ return gtsam::serialize(*self); })
        .def("deserialize", [](gtsam::Point3* self, string serialized){ gtsam::deserialize(serialized, *self); }, py::arg("serialized"))
        .def(py::pickle(
            [](const gtsam::Point3 &a){ /* __getstate__: Returns a string that encodes the state of the object */ return py::make_tuple(gtsam::serialize(a)); },
            [](py::tuple t){ /* __setstate__ */ gtsam::Point3 obj; gtsam::deserialize(t[0].cast<std::string>(), obj); return obj; }))
        .def_static("staticFunction",&gtwrap_generated_adapters::callable_15)
        .def_static("StaticFunctionRet",&gtwrap_generated_adapters::callable_16, gtwrap::internal::py_arg<double>("z"));


#include "python/specializations.h"

}

