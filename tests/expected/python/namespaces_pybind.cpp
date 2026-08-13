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




using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(namespaces_py, m_) {
    m_.doc() = "pybind11 wrapper of namespaces_py";


    // Named adapters avoid a unique callable type per binding.
    struct gtwrap_generated_adapters {
        static auto callable_0() -> std::decay<decltype(ns1::aGlobalFunction())>::type { return ns1::aGlobalFunction(); }
        static auto callable_1(ns2::ClassA* self) -> std::decay<decltype(self->memberFunction())>::type { return self->memberFunction(); }
        static auto callable_2(ns2::ClassA* self, const ns1::ClassB& arg) -> std::decay<decltype(self->nsArg(arg))>::type { return self->nsArg(arg); }
        static auto callable_3(ns2::ClassA* self, double q) -> std::decay<decltype(self->nsReturn(q))>::type { return self->nsReturn(q); }
        static auto callable_4() -> std::decay<decltype(ns2::ClassA::afunction())>::type { return ns2::ClassA::afunction(); }
        static auto callable_5() -> std::decay<decltype(ns2::aGlobalFunction())>::type { return ns2::aGlobalFunction(); }
        static auto callable_6(const ns1::ClassA& a) -> std::decay<decltype(ns2::overloadedGlobalFunction(a))>::type { return ns2::overloadedGlobalFunction(a); }
        static auto callable_7(const ns1::ClassA& a, double b) -> std::decay<decltype(ns2::overloadedGlobalFunction(a, b))>::type { return ns2::overloadedGlobalFunction(a, b); }
        static void callable_8(gtsam::Values* self, size_t j, const gtsam::Vector& vector) { self->insert(j, vector); }
        static void callable_9(gtsam::Values* self, size_t j, const gtsam::Vector& vector) { self->insert(j, vector); }
        static void callable_10(gtsam::Values* self, size_t j, const gtsam::Matrix& matrix) { self->insert(j, matrix); }
        static void callable_11(gtsam::Values* self, size_t j, const gtsam::Matrix& matrix) { self->insert(j, matrix); }
    };
    pybind11::module m_ns1 = m_.def_submodule("ns1", "ns1 submodule");

    py::class_<ns1::ClassA, std::shared_ptr<ns1::ClassA>>(m_ns1, "ClassA")
        .def(py::init<>());

    py::class_<ns1::ClassB, std::shared_ptr<ns1::ClassB>>(m_ns1, "ClassB")
        .def(py::init<>());

    m_ns1.def("aGlobalFunction",&gtwrap_generated_adapters::callable_0);    pybind11::module m_ns2 = m_.def_submodule("ns2", "ns2 submodule");

    py::class_<ns2::ClassA, std::shared_ptr<ns2::ClassA>>(m_ns2, "ClassA")
        .def(py::init<>())
        .def("memberFunction",&gtwrap_generated_adapters::callable_1)
        .def("nsArg",&gtwrap_generated_adapters::callable_2, gtwrap::internal::py_arg<const ns1::ClassB&>("arg"))
        .def("nsReturn",&gtwrap_generated_adapters::callable_3, gtwrap::internal::py_arg<double>("q"))
        .def_static("afunction",&gtwrap_generated_adapters::callable_4);
    pybind11::module m_ns2_ns3 = m_ns2.def_submodule("ns3", "ns3 submodule");

    py::class_<ns2::ns3::ClassB, std::shared_ptr<ns2::ns3::ClassB>>(m_ns2_ns3, "ClassB")
        .def(py::init<>());

    py::class_<ns2::ClassC, std::shared_ptr<ns2::ClassC>>(m_ns2, "ClassC")
        .def(py::init<>());

    m_ns2.attr("aNs2Var") = ns2::aNs2Var;
    m_ns2.def("aGlobalFunction",&gtwrap_generated_adapters::callable_5);
    m_ns2.def("overloadedGlobalFunction",&gtwrap_generated_adapters::callable_6, gtwrap::internal::py_arg<const ns1::ClassA&>("a"));
    m_ns2.def("overloadedGlobalFunction",&gtwrap_generated_adapters::callable_7, gtwrap::internal::py_arg<const ns1::ClassA&>("a"), gtwrap::internal::py_arg<double>("b"));
    py::class_<ClassD, std::shared_ptr<ClassD>>(m_, "ClassD")
        .def(py::init<>());

    m_.attr("aGlobalVar") = aGlobalVar;    pybind11::module m_gtsam = m_.def_submodule("gtsam", "gtsam submodule");

    py::class_<gtsam::Values, std::shared_ptr<gtsam::Values>>(m_gtsam, "Values")
        .def(py::init<>())
        .def(py::init<const gtsam::Values&>(), gtwrap::internal::py_arg<const gtsam::Values&>("other"))
        .def("insert_vector",&gtwrap_generated_adapters::callable_8, gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Vector&>("vector"))
        .def("insert",&gtwrap_generated_adapters::callable_9, gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Vector&>("vector"))
        .def("insert_matrix",&gtwrap_generated_adapters::callable_10, gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Matrix&>("matrix"))
        .def("insert",&gtwrap_generated_adapters::callable_11, gtwrap::internal::py_arg<size_t>("j"), gtwrap::internal::py_arg<const gtsam::Matrix&>("matrix"));


#include "python/specializations.h"

}

