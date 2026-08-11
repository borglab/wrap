#include <pybind11/pybind11.h>

#include "pybind_lambda_adapters.h"

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

PYBIND11_MODULE(pybind_lambda_adapters_py, m_) {
    pybind11::module m_adapters = m_.def_submodule("adapters", "adapters submodule");

    py::class_<adapters::BaseAdapter, std::shared_ptr<adapters::BaseAdapter>>(m_adapters, "BaseAdapter")
        .def(py::init<>())
        .def("inherited",[](adapters::BaseAdapter* self, int value){return self->inherited(value);}, gtwrap::internal::py_arg<int>("value"));

    py::class_<adapters::Adapter<int>, adapters::BaseAdapter, std::shared_ptr<adapters::Adapter<int>>>(m_adapters, "AdapterInt")
        .def(py::init<>())
        .def("exact",&adapters::Adapter<int>::exact, gtwrap::internal::py_arg<int>("value"))
        .def("exactConst",&adapters::Adapter<int>::exactConst, gtwrap::internal::py_arg<int>("value"))
        .def("omittedDefault",[](adapters::Adapter<int>* self, int value){return self->omittedDefault(value);}, gtwrap::internal::py_arg<int>("value"))
        .def("referenceArgument",[](adapters::Adapter<int>* self, int value){return self->referenceArgument(value);}, gtwrap::internal::py_arg<int>("value"))
        .def("hiddenOverload",[](adapters::Adapter<int>* self, int value){return self->hiddenOverload(value);}, gtwrap::internal::py_arg<int>("value"))
        .def("declaredOverload",[](adapters::Adapter<int>* self, int value){return self->declaredOverload(value);}, gtwrap::internal::py_arg<int>("value"))
        .def("declaredOverload",py::overload_cast<double>(&adapters::Adapter<int>::declaredOverload, py::const_), gtwrap::internal::py_arg<double>("value"))
        .def("at",[](adapters::Adapter<int>* self, size_t index){return self->at(index);}, gtwrap::internal::py_arg<size_t>("index"))
        .def("front",[](adapters::Adapter<int>* self){return self->front();})
        .def("alias",[](adapters::Adapter<int>* self, int index){return self->alias(index);}, gtwrap::internal::py_arg<int>("index"))
        .def("templatedDouble",[](adapters::Adapter<int>* self, double value){return self->templated<double>(value);}, gtwrap::internal::py_arg<double>("value"))
        .def("lambda_",[](adapters::Adapter<int>* self, const string& value) -> const auto&{return self->lambda(value);}, py::return_value_policy::reference_internal, gtwrap::internal::py_arg<const string&>("value") = "fallback")
        .def_static("exactStatic",&adapters::Adapter<int>::exactStatic, gtwrap::internal::py_arg<int>("value"))
        .def_static("staticOmitted",[](int value){return adapters::Adapter<int>::staticOmitted(value);}, gtwrap::internal::py_arg<int>("value"));

    m_adapters.def("exactGlobal",&adapters::exactGlobal, gtwrap::internal::py_arg<int>("value"));
    m_adapters.def("globalOmitted",[](int value){return adapters::globalOmitted(value);}, gtwrap::internal::py_arg<int>("value"));
    m_adapters.def("globalHidden",[](int value){return adapters::globalHidden(value);}, gtwrap::internal::py_arg<int>("value"));
    m_adapters.def("globalOverload",[](int value){return adapters::globalOverload(value);}, gtwrap::internal::py_arg<int>("value"));
    m_adapters.def("globalOverload",py::overload_cast<double>(&adapters::globalOverload), gtwrap::internal::py_arg<double>("value"));
    m_adapters.def("globalTemplatedInt",[](int value){return adapters::globalTemplated<int>(value);}, gtwrap::internal::py_arg<int>("value"));
}
