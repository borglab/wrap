

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

    py::enum_<Color>(m_, "Color", py::arithmetic())
        .value("Red", Color::Red)
        .value("Green", Color::Green)
        .value("Blue", Color::Blue);


    py::class_<Pet, std::shared_ptr<Pet>>(m_, "Pet")
        .def(py::init<const string&, Kind>(), py::arg("name"), py::arg("type"))
        .def_readwrite("name", &Pet::name)
        .def_readwrite("type", &Pet::type);

    py::enum_<Pet::Kind>(m_, "Kind", py::arithmetic())
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


    py::class_<gtsam::MCU, std::shared_ptr<gtsam::MCU>>(m_gtsam, "MCU")
        .def(py::init<>());

    py::enum_<MCU::Avengers>(m_, "Avengers", py::arithmetic())
        .value("CaptainAmerica", MCU::Avengers::CaptainAmerica)
        .value("IronMan", MCU::Avengers::IronMan)
        .value("Hulk", MCU::Avengers::Hulk)
        .value("Hawkeye", MCU::Avengers::Hawkeye)
        .value("Thor", MCU::Avengers::Thor);


    py::enum_<MCU::GotG>(m_, "GotG", py::arithmetic())
        .value("Starlord", MCU::GotG::Starlord)
        .value("Gamorra", MCU::GotG::Gamorra)
        .value("Rocket", MCU::GotG::Rocket)
        .value("Drax", MCU::GotG::Drax)
        .value("Groot", MCU::GotG::Groot);



#include "python/specializations.h"

}

