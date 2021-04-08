

#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.

#include "folder/path/to/Test.h"

#include "wrap/serialization.h"
#include <boost/serialization/export.hpp>





using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(class_py, m_) {
    m_.doc() = "pybind11 wrapper of class_py";


    py::class_<FunRange, std::shared_ptr<FunRange>>(m_, "FunRange")
        .def(py::init<>())
        .def("range",[](FunRange* self, double d){return self->range(d);}, py::arg("d"))
        .def_static("create",[](){return FunRange::create();});

    py::class_<Fun<double>, std::shared_ptr<Fun<double>>>(m_, "FunDouble")
        .def("templatedMethodString",[](Fun<double>* self, double d, string t){return self->templatedMethod<string>(d, t);}, py::arg("d"), py::arg("t"))
        .def("multiTemplatedMethodStringSize_t",[](Fun<double>* self, double d, string t, size_t u){return self->multiTemplatedMethod<string,size_t>(d, t, u);}, py::arg("d"), py::arg("t"), py::arg("u"))
        .def_static("staticMethodWithThis",[](){return Fun<double>::staticMethodWithThis();});

    py::class_<Test, std::shared_ptr<Test>>(m_, "Test")
        .def(py::init<>())
        .def(py::init<double, const gtsam::Matrix&>(), py::arg("a"), py::arg("b"))
        .def("return_pair",[](Test* self, const gtsam::Vector& v, const gtsam::Matrix& A){return self->return_pair(v, A);}, py::arg("v"), py::arg("A"))
        .def("return_pair",[](Test* self, const gtsam::Vector& v){return self->return_pair(v);}, py::arg("v"))
        .def("return_bool",[](Test* self, bool value){return self->return_bool(value);}, py::arg("value"))
        .def("return_size_t",[](Test* self, size_t value){return self->return_size_t(value);}, py::arg("value"))
        .def("return_int",[](Test* self, int value){return self->return_int(value);}, py::arg("value"))
        .def("return_double",[](Test* self, double value){return self->return_double(value);}, py::arg("value"))
        .def("return_string",[](Test* self, string value){return self->return_string(value);}, py::arg("value"))
        .def("return_vector1",[](Test* self, const gtsam::Vector& value){return self->return_vector1(value);}, py::arg("value"))
        .def("return_matrix1",[](Test* self, const gtsam::Matrix& value){return self->return_matrix1(value);}, py::arg("value"))
        .def("return_vector2",[](Test* self, const gtsam::Vector& value){return self->return_vector2(value);}, py::arg("value"))
        .def("return_matrix2",[](Test* self, const gtsam::Matrix& value){return self->return_matrix2(value);}, py::arg("value"))
        .def("arg_EigenConstRef",[](Test* self, const gtsam::Matrix& value){ self->arg_EigenConstRef(value);}, py::arg("value"))
        .def("return_field",[](Test* self, const Test& t){return self->return_field(t);}, py::arg("t"))
        .def("return_TestPtr",[](Test* self, const std::shared_ptr<Test> value){return self->return_TestPtr(value);}, py::arg("value"))
        .def("return_Test",[](Test* self, std::shared_ptr<Test> value){return self->return_Test(value);}, py::arg("value"))
        .def("return_Point2Ptr",[](Test* self, bool value){return self->return_Point2Ptr(value);}, py::arg("value"))
        .def("create_ptrs",[](Test* self){return self->create_ptrs();})
        .def("create_MixedPtrs",[](Test* self){return self->create_MixedPtrs();})
        .def("return_ptrs",[](Test* self, std::shared_ptr<Test> p1, std::shared_ptr<Test> p2){return self->return_ptrs(p1, p2);}, py::arg("p1"), py::arg("p2"))
        .def("print_",[](Test* self, const string& s, const gtsam::KeyFormatter& keyFormatter){ self->print(s, keyFormatter);}, py::arg("s"), py::arg("keyFormatter"))
        .def("__repr__",
                    [](const Test &a, const string& s, const gtsam::KeyFormatter& keyFormatter) {
                        gtsam::RedirectCout redirect;
                        a.print(s, keyFormatter);
                        return redirect.str();
                    }, py::arg("s") = "", py::arg("keyFormatter") = gtsam::DefaultKeyFormatter)
        .def("set_container",[](Test* self, std::vector<testing::Test> container){ self->set_container(container);}, py::arg("container"))
        .def("set_container",[](Test* self, std::vector<std::shared_ptr<testing::Test>> container){ self->set_container(container);}, py::arg("container"))
        .def("set_container",[](Test* self, std::vector<testing::Test&> container){ self->set_container(container);}, py::arg("container"))
        .def("get_container",[](Test* self){return self->get_container();})
        .def_readwrite("model_ptr", &Test::model_ptr);

    py::class_<PrimitiveRef<double>, std::shared_ptr<PrimitiveRef<double>>>(m_, "PrimitiveRefDouble")
        .def(py::init<>())
        .def_static("Brutal",[](const double& t){return PrimitiveRef<double>::Brutal(t);}, py::arg("t"));

    py::class_<MyVector<3>, std::shared_ptr<MyVector<3>>>(m_, "MyVector3")
        .def(py::init<>());

    py::class_<MyVector<12>, std::shared_ptr<MyVector<12>>>(m_, "MyVector12")
        .def(py::init<>());

    py::class_<MultipleTemplates<int, double>, std::shared_ptr<MultipleTemplates<int, double>>>(m_, "MultipleTemplatesIntDouble");

    py::class_<MultipleTemplates<int, float>, std::shared_ptr<MultipleTemplates<int, float>>>(m_, "MultipleTemplatesIntFloat");

    py::class_<MyFactor<gtsam::Pose2, gtsam::Matrix>, std::shared_ptr<MyFactor<gtsam::Pose2, gtsam::Matrix>>>(m_, "MyFactorPosePoint2")
        .def(py::init<size_t, size_t, double, const std::shared_ptr<gtsam::noiseModel::Base>>(), py::arg("key1"), py::arg("key2"), py::arg("measured"), py::arg("noiseModel"));


#include "python/specializations.h"

}

