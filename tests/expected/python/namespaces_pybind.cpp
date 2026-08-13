#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.

#include "path/to/ns1.h"
#include "path/to/ns1/ClassB.h"
#include "path/to/ns2.h"
#include "path/to/ns2/ClassA.h"
#include "path/to/ns3.h"
#include "gtsam/nonlinear/Values.h"

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




using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(namespaces_py, m_) {
    m_.doc() = "pybind11 wrapper of namespaces_py";

    pybind11::module m_ns1 = m_.def_submodule("ns1", "ns1 submodule");

    py::class_<ns1::ClassA, std::shared_ptr<ns1::ClassA>>(m_ns1, "ClassA")
        .def(py::init<>());

    py::class_<ns1::ClassB, std::shared_ptr<ns1::ClassB>>(m_ns1, "ClassB")
        .def(py::init<>());

    m_ns1.def("aGlobalFunction",gtwrap::internal::SelectOverload<>::function(&ns1::aGlobalFunction));    pybind11::module m_ns2 = m_.def_submodule("ns2", "ns2 submodule");

    py::class_<ns2::ClassA, std::shared_ptr<ns2::ClassA>>(m_ns2, "ClassA")
        .def(py::init<>())
        .def("memberFunction",gtwrap::internal::SelectOverload<>::method(&ns2::ClassA::memberFunction))
        .def("nsArg",gtwrap::internal::SelectOverload<const ns1::ClassB&>::method(&ns2::ClassA::nsArg), gtwrap::internal::py_arg<const ns1::ClassB&>("arg"))
        .def("nsReturn",gtwrap::internal::SelectOverload<double>::method(&ns2::ClassA::nsReturn), gtwrap::internal::py_arg<double>("q"))
        .def_static("afunction",gtwrap::internal::SelectOverload<>::function(&ns2::ClassA::afunction));
    pybind11::module m_ns2_ns3 = m_ns2.def_submodule("ns3", "ns3 submodule");

    py::class_<ns2::ns3::ClassB, std::shared_ptr<ns2::ns3::ClassB>>(m_ns2_ns3, "ClassB")
        .def(py::init<>());

    py::class_<ns2::ClassC, std::shared_ptr<ns2::ClassC>>(m_ns2, "ClassC")
        .def(py::init<>());

    m_ns2.attr("aNs2Var") = ns2::aNs2Var;
    m_ns2.def("aGlobalFunction",gtwrap::internal::SelectOverload<>::function(&ns2::aGlobalFunction));
    m_ns2.def("overloadedGlobalFunction",gtwrap::internal::SelectOverload<const ns1::ClassA&>::function(&ns2::overloadedGlobalFunction), gtwrap::internal::py_arg<const ns1::ClassA&>("a"));
    m_ns2.def("overloadedGlobalFunction",gtwrap::internal::SelectOverload<const ns1::ClassA&, double>::function(&ns2::overloadedGlobalFunction), gtwrap::internal::py_arg<const ns1::ClassA&>("a"), gtwrap::internal::py_arg<double>("b"));
    py::class_<ClassD, std::shared_ptr<ClassD>>(m_, "ClassD")
        .def(py::init<>());

    m_.attr("aGlobalVar") = aGlobalVar;    pybind11::module m_gtsam = m_.def_submodule("gtsam", "gtsam submodule");

    py::class_<gtsam::Values, std::shared_ptr<gtsam::Values>>(m_gtsam, "Values")
        .def(py::init<>())
        .def(py::init<const gtsam::Values&>(), gtwrap::internal::py_arg<const gtsam::Values&>("other"))
        .def("insert_vector",gtwrap::internal::SelectOverload<size_t, const gtsam::Vector&>::method(&gtsam::Values::insert), gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Vector&>("vector"))
        .def("insert",gtwrap::internal::SelectOverload<size_t, const gtsam::Vector&>::method(&gtsam::Values::insert), gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Vector&>("vector"))
        .def("insert_matrix",gtwrap::internal::SelectOverload<size_t, const gtsam::Matrix&>::method(&gtsam::Values::insert), gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Matrix&>("matrix"))
        .def("insert",gtwrap::internal::SelectOverload<size_t, const gtsam::Matrix&>::method(&gtsam::Values::insert), gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Matrix&>("matrix"));


#include "python/specializations.h"

}

