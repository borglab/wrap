#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.


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

PYBIND11_MODULE(enum_py, m_) {
    m_.doc() = "pybind11 wrapper of enum_py";


    // Named adapters avoid a unique callable type per binding.
    struct gtwrap_generated_adapters {
        static void callable_0(Pet* self, const Color& color) { self->setColor(color); }
        static auto callable_1(Pet* self) -> std::decay<decltype(self->getColor())>::type { return self->getColor(); }
        static void callable_2(gtsam::Optimizer<gtsam::GaussNewtonParams>* self, const Optimizer<gtsam::GaussNewtonParams>::Verbosity value) { self->setVerbosity(value); }
        static auto callable_3(gtsam::Optimizer<gtsam::GaussNewtonParams>* self) -> std::decay<decltype(self->getVerbosity())>::type { return self->getVerbosity(); }
        static auto callable_4(gtsam::Optimizer<gtsam::GaussNewtonParams>* self) -> std::decay<decltype(self->getVerbosity())>::type { return self->getVerbosity(); }
    };
    py::enum_<Color>(m_, "Color", py::arithmetic())
        .value("Red", Color::Red)
        .value("Green", Color::Green)
        .value("Blue", Color::Blue);


    py::class_<Pet, std::shared_ptr<Pet>> pet(m_, "Pet");
    pet
        .def(py::init<const string&, Pet::Kind>(), gtwrap::internal::py_arg<const string&>("name"), gtwrap::internal::py_arg<Pet::Kind>("type"))
        .def("setColor",&gtwrap_generated_adapters::callable_0, gtwrap::internal::py_arg<const Color&>("color"))
        .def("getColor",&gtwrap_generated_adapters::callable_1)
        .def_readwrite("name", &Pet::name)
        .def_readwrite("type", &Pet::type);

    py::enum_<Pet::Kind>(pet, "Kind", py::arithmetic())
        .value("Dog", Pet::Kind::Dog)
        .value("Cat", Pet::Kind::Cat);

    pybind11::module m_gtsam = m_.def_submodule("gtsam", "gtsam submodule");
    py::enum_<gtsam::VerbosityLM>(m_gtsam, "VerbosityLM", py::arithmetic())
        .value("SILENT", gtsam::VerbosityLM::SILENT)
        .value("SUMMARY", gtsam::VerbosityLM::SUMMARY)
        .value("TERMINATION", gtsam::VerbosityLM::TERMINATION)
        .value("LAMBDA", gtsam::VerbosityLM::LAMBDA)
        .value("TRYLAMBDA", gtsam::VerbosityLM::TRYLAMBDA)
        .value("TRYCONFIG", gtsam::VerbosityLM::TRYCONFIG)
        .value("DAMPED", gtsam::VerbosityLM::DAMPED)
        .value("TRYDELTA", gtsam::VerbosityLM::TRYDELTA);


    py::class_<gtsam::MCU, std::shared_ptr<gtsam::MCU>> mcu(m_gtsam, "MCU");
    mcu
        .def(py::init<>());

    py::enum_<gtsam::MCU::Avengers>(mcu, "Avengers", py::arithmetic())
        .value("CaptainAmerica", gtsam::MCU::Avengers::CaptainAmerica)
        .value("IronMan", gtsam::MCU::Avengers::IronMan)
        .value("Hulk", gtsam::MCU::Avengers::Hulk)
        .value("Hawkeye", gtsam::MCU::Avengers::Hawkeye)
        .value("Thor", gtsam::MCU::Avengers::Thor);


    py::enum_<gtsam::MCU::GotG>(mcu, "GotG", py::arithmetic())
        .value("Starlord", gtsam::MCU::GotG::Starlord)
        .value("Gamorra", gtsam::MCU::GotG::Gamorra)
        .value("Rocket", gtsam::MCU::GotG::Rocket)
        .value("Drax", gtsam::MCU::GotG::Drax)
        .value("Groot", gtsam::MCU::GotG::Groot);


    py::class_<gtsam::Optimizer<gtsam::GaussNewtonParams>, std::shared_ptr<gtsam::Optimizer<gtsam::GaussNewtonParams>>> optimizergaussnewtonparams(m_gtsam, "OptimizerGaussNewtonParams");
    optimizergaussnewtonparams
        .def(py::init<const Optimizer<gtsam::GaussNewtonParams>::Verbosity&>(), gtwrap::internal::py_arg<const Optimizer<gtsam::GaussNewtonParams>::Verbosity&>("verbosity"))
        .def("setVerbosity",&gtwrap_generated_adapters::callable_2, gtwrap::internal::py_arg<const Optimizer<gtsam::GaussNewtonParams>::Verbosity>("value"))
        .def("getVerbosity",&gtwrap_generated_adapters::callable_3)
        .def("getVerbosity",&gtwrap_generated_adapters::callable_4);

    py::enum_<gtsam::Optimizer<gtsam::GaussNewtonParams>::Verbosity>(optimizergaussnewtonparams, "Verbosity", py::arithmetic())
        .value("SILENT", gtsam::Optimizer<gtsam::GaussNewtonParams>::Verbosity::SILENT)
        .value("SUMMARY", gtsam::Optimizer<gtsam::GaussNewtonParams>::Verbosity::SUMMARY)
        .value("VERBOSE", gtsam::Optimizer<gtsam::GaussNewtonParams>::Verbosity::VERBOSE);



#include "python/specializations.h"

}

