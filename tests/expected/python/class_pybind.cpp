#include <pybind11/eigen.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "gtsam/nonlinear/utilities.h"  // for RedirectCout.

#include "folder/path/to/Test.h"

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

PYBIND11_MODULE(class_py, m_) {
    m_.doc() = "pybind11 wrapper of class_py";


    // Named adapters avoid a unique callable type per binding.
    struct gtwrap_generated_adapters {
        static auto callable_0(FunRange* self, double d) -> std::decay<decltype(self->range(d))>::type { return self->range(d); }
        static auto callable_1() -> std::decay<decltype(FunRange::create())>::type { return FunRange::create(); }
        static auto callable_2(Fun<double>* self, double d, string t) -> std::decay<decltype(self->templatedMethod<string>(d, t))>::type { return self->templatedMethod<string>(d, t); }
        static auto callable_3(Fun<double>* self, double d, string t, size_t u) -> std::decay<decltype(self->multiTemplatedMethod<string,size_t>(d, t, u))>::type { return self->multiTemplatedMethod<string,size_t>(d, t, u); }
        static auto callable_4(Fun<double>* self) -> std::decay<decltype(self->sets())>::type { return self->sets(); }
        static auto callable_5() -> std::decay<decltype(Fun<double>::staticMethodWithThis())>::type { return Fun<double>::staticMethodWithThis(); }
        static auto callable_6(const int& m) -> std::decay<decltype(Fun<double>::templatedStaticMethod<int>(m))>::type { return Fun<double>::templatedStaticMethod<int>(m); }
        static auto callable_7(Test* self, const gtsam::Vector& v, const gtsam::Matrix& A) -> std::decay<decltype(self->return_pair(v, A))>::type { return self->return_pair(v, A); }
        static auto callable_8(Test* self, const gtsam::Vector& v) -> std::decay<decltype(self->return_pair(v))>::type { return self->return_pair(v); }
        static auto callable_9(Test* self, bool value) -> std::decay<decltype(self->return_bool(value))>::type { return self->return_bool(value); }
        static auto callable_10(Test* self, size_t value) -> std::decay<decltype(self->return_size_t(value))>::type { return self->return_size_t(value); }
        static auto callable_11(Test* self, int value) -> std::decay<decltype(self->return_int(value))>::type { return self->return_int(value); }
        static auto callable_12(Test* self, double value) -> std::decay<decltype(self->return_double(value))>::type { return self->return_double(value); }
        static auto callable_13(Test* self, string value) -> std::decay<decltype(self->return_string(value))>::type { return self->return_string(value); }
        static auto callable_14(Test* self, const gtsam::Vector& value) -> std::decay<decltype(self->return_vector1(value))>::type { return self->return_vector1(value); }
        static auto callable_15(Test* self, const gtsam::Matrix& value) -> std::decay<decltype(self->return_matrix1(value))>::type { return self->return_matrix1(value); }
        static auto callable_16(Test* self, const gtsam::Vector& value) -> std::decay<decltype(self->return_vector2(value))>::type { return self->return_vector2(value); }
        static auto callable_17(Test* self, const gtsam::Matrix& value) -> std::decay<decltype(self->return_matrix2(value))>::type { return self->return_matrix2(value); }
        static auto callable_18(Test* self, const gtsam::Vector& value) -> std::remove_reference<decltype(self->return_vector2(value))>::type const& { return self->return_vector2(value); }
        static auto callable_19(Test* self, const gtsam::Matrix& value) -> std::remove_reference<decltype(self->return_matrix2(value))>::type const& { return self->return_matrix2(value); }
        static void callable_20(Test* self, const gtsam::Matrix& value) { self->arg_EigenConstRef(value); }
        static void callable_21(Test* self, gtsam::Key key) { self->push_back(key); }
        static auto callable_22(Test* self, const Test& t) -> std::decay<decltype(self->return_field(t))>::type { return self->return_field(t); }
        static auto callable_23(Test* self, const std::shared_ptr<Test> value) -> std::decay<decltype(self->return_TestPtr(value))>::type { return self->return_TestPtr(value); }
        static auto callable_24(Test* self, std::shared_ptr<Test> value) -> std::decay<decltype(self->return_Test(value))>::type { return self->return_Test(value); }
        static auto callable_25(Test* self, bool value) -> std::decay<decltype(self->return_Point2Ptr(value))>::type { return self->return_Point2Ptr(value); }
        static auto callable_26(Test* self) -> std::decay<decltype(self->create_ptrs())>::type { return self->create_ptrs(); }
        static auto callable_27(Test* self) -> std::decay<decltype(self->create_MixedPtrs())>::type { return self->create_MixedPtrs(); }
        static auto callable_28(Test* self, std::shared_ptr<Test> p1, std::shared_ptr<Test> p2) -> std::decay<decltype(self->return_ptrs(p1, p2))>::type { return self->return_ptrs(p1, p2); }
        static void callable_29(Test* self) { self->lambda(); }
        static void callable_30(Test* self, std::vector<testing::Test> container) { self->set_container(container); }
        static void callable_31(Test* self, std::vector<std::shared_ptr<testing::Test>> container) { self->set_container(container); }
        static void callable_32(Test* self, std::vector<testing::Test&> container) { self->set_container(container); }
        static auto callable_33(Test* self) -> std::decay<decltype(self->get_container())>::type { return self->get_container(); }
        static auto callable_34(Test* self, const gtsam::KeyFormatter& keyFormatter) -> std::decay<decltype(self->markdown(keyFormatter))>::type { return self->markdown(keyFormatter); }
        static auto callable_35(const double& t) -> std::decay<decltype(PrimitiveRef<double>::Brutal(t))>::type { return PrimitiveRef<double>::Brutal(t); }
        static void callable_36(SmartProjectionRigFactor<gtsam::PinholeCamera<gtsam::Cal3_S2>>* self, const gtsam::PinholeCamera<gtsam::Cal3_S2>::Measurement& measured, const gtsam::Key& poseKey, const size_t& cameraId) { self->add(measured, poseKey, cameraId); }
    };

    py::class_<FunRange, std::shared_ptr<FunRange>>(m_, "FunRange")
        .def(py::init<>())
        .def("range",&gtwrap_generated_adapters::callable_0, gtwrap::internal::py_arg<double>("d"))
        .def_static("create",&gtwrap_generated_adapters::callable_1);

    py::class_<Fun<double>, std::shared_ptr<Fun<double>>>(m_, "FunDouble")
        .def("templatedMethodString",&gtwrap_generated_adapters::callable_2, gtwrap::internal::py_arg<double>("d"), gtwrap::internal::py_arg<string>("t"))
        .def("multiTemplatedMethodStringSize_t",&gtwrap_generated_adapters::callable_3, gtwrap::internal::py_arg<double>("d"), gtwrap::internal::py_arg<string>("t"), gtwrap::internal::py_arg<size_t>("u"))
        .def("sets",&gtwrap_generated_adapters::callable_4)
        .def_static("staticMethodWithThis",&gtwrap_generated_adapters::callable_5)
        .def_static("templatedStaticMethodInt",&gtwrap_generated_adapters::callable_6, gtwrap::internal::py_arg<const int&>("m"));

    py::class_<Test, std::shared_ptr<Test>>(m_, "Test")
        .def(py::init<>())
        .def(py::init<double, const gtsam::Matrix&>(), gtwrap::internal::py_arg<double>("a"), gtwrap::internal::py_arg<const gtsam::Matrix&>("b"))
        .def("return_pair",&gtwrap_generated_adapters::callable_7, gtwrap::internal::py_arg<const gtsam::Vector&>("v"), gtwrap::internal::py_arg<const gtsam::Matrix&>("A"))
        .def("return_pair",&gtwrap_generated_adapters::callable_8, gtwrap::internal::py_arg<const gtsam::Vector&>("v"))
        .def("return_bool",&gtwrap_generated_adapters::callable_9, gtwrap::internal::py_arg<bool>("value"))
        .def("return_size_t",&gtwrap_generated_adapters::callable_10, gtwrap::internal::py_arg<size_t>("value"))
        .def("return_int",&gtwrap_generated_adapters::callable_11, gtwrap::internal::py_arg<int>("value"))
        .def("return_double",&gtwrap_generated_adapters::callable_12, gtwrap::internal::py_arg<double>("value"))
        .def("return_string",&gtwrap_generated_adapters::callable_13, gtwrap::internal::py_arg<string>("value"))
        .def("return_vector1",&gtwrap_generated_adapters::callable_14, gtwrap::internal::py_arg<const gtsam::Vector&>("value"))
        .def("return_matrix1",&gtwrap_generated_adapters::callable_15, gtwrap::internal::py_arg<const gtsam::Matrix&>("value"))
        .def("return_vector2",&gtwrap_generated_adapters::callable_16, gtwrap::internal::py_arg<const gtsam::Vector&>("value"))
        .def("return_matrix2",&gtwrap_generated_adapters::callable_17, gtwrap::internal::py_arg<const gtsam::Matrix&>("value"))
        .def("return_vector2",&gtwrap_generated_adapters::callable_18, py::return_value_policy::reference_internal, gtwrap::internal::py_arg<const gtsam::Vector&>("value"))
        .def("return_matrix2",&gtwrap_generated_adapters::callable_19, py::return_value_policy::reference_internal, gtwrap::internal::py_arg<const gtsam::Matrix&>("value"))
        .def("arg_EigenConstRef",&gtwrap_generated_adapters::callable_20, gtwrap::internal::py_arg<const gtsam::Matrix&>("value"))
        .def("push_back",&gtwrap_generated_adapters::callable_21, gtwrap::internal::py_arg<gtsam::Key>("key"))
        .def("return_field",&gtwrap_generated_adapters::callable_22, gtwrap::internal::py_arg<const Test&>("t"))
        .def("return_TestPtr",&gtwrap_generated_adapters::callable_23, gtwrap::internal::py_arg<const std::shared_ptr<Test>>("value"))
        .def("return_Test",&gtwrap_generated_adapters::callable_24, gtwrap::internal::py_arg<std::shared_ptr<Test>>("value"))
        .def("return_Point2Ptr",&gtwrap_generated_adapters::callable_25, gtwrap::internal::py_arg<bool>("value"))
        .def("create_ptrs",&gtwrap_generated_adapters::callable_26)
        .def("create_MixedPtrs",&gtwrap_generated_adapters::callable_27)
        .def("return_ptrs",&gtwrap_generated_adapters::callable_28, gtwrap::internal::py_arg<std::shared_ptr<Test>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<Test>>("p2"))
        .def("print",[](Test* self){ py::scoped_ostream_redirect output; self->print();})
        .def("__repr__",
                    [](const Test& self){
                        gtsam::RedirectCout redirect;
                        self.print();
                        return redirect.str();
                    })
        .def("lambda_",&gtwrap_generated_adapters::callable_29)
        .def("set_container",&gtwrap_generated_adapters::callable_30, gtwrap::internal::py_arg<std::vector<testing::Test>>("container"))
        .def("set_container",&gtwrap_generated_adapters::callable_31, gtwrap::internal::py_arg<std::vector<std::shared_ptr<testing::Test>>>("container"))
        .def("set_container",&gtwrap_generated_adapters::callable_32, gtwrap::internal::py_arg<std::vector<testing::Test&>>("container"))
        .def("get_container",&gtwrap_generated_adapters::callable_33)
        .def("_repr_markdown_",&gtwrap_generated_adapters::callable_34, gtwrap::internal::py_arg<const gtsam::KeyFormatter&>("keyFormatter") = gtsam::DefaultKeyFormatter)
        .def_readwrite("model_ptr", &Test::model_ptr)
        .def_readwrite("value", &Test::value)
        .def_readwrite("name", &Test::name);

    py::class_<PrimitiveRef<double>, std::shared_ptr<PrimitiveRef<double>>>(m_, "PrimitiveRefDouble")
        .def(py::init<>())
        .def_static("Brutal",&gtwrap_generated_adapters::callable_35, gtwrap::internal::py_arg<const double&>("t"));

    py::class_<MyVector<3>, std::shared_ptr<MyVector<3>>>(m_, "MyVector3")
        .def(py::init<>());

    py::class_<MyVector<12>, std::shared_ptr<MyVector<12>>>(m_, "MyVector12")
        .def(py::init<>());

    py::class_<MultipleTemplates<int, double>, std::shared_ptr<MultipleTemplates<int, double>>>(m_, "MultipleTemplatesIntDouble");

    py::class_<MultipleTemplates<int, float>, std::shared_ptr<MultipleTemplates<int, float>>>(m_, "MultipleTemplatesIntFloat");

    py::class_<ForwardKinematics, std::shared_ptr<ForwardKinematics>>(m_, "ForwardKinematics")
        .def(py::init<const gtdynamics::Robot&, const string&, const string&, const gtsam::Values&, const gtsam::Pose3&>(), gtwrap::internal::py_arg<const gtdynamics::Robot&>("robot"), gtwrap::internal::py_arg<const string&>("start_link_name"), gtwrap::internal::py_arg<const string&>("end_link_name"), gtwrap::internal::py_arg<const gtsam::Values&>("joint_angles"), gtwrap::internal::py_arg<const gtsam::Pose3&>("l2Tp") = gtsam::Pose3());

    py::class_<TemplatedConstructor, std::shared_ptr<TemplatedConstructor>>(m_, "TemplatedConstructor")
        .def(py::init<>())
        .def(py::init<const string&>(), gtwrap::internal::py_arg<const string&>("arg"))
        .def(py::init<const int&>(), gtwrap::internal::py_arg<const int&>("arg"))
        .def(py::init<const double&>(), gtwrap::internal::py_arg<const double&>("arg"));

    py::class_<FastSet, std::shared_ptr<FastSet>>(m_, "FastSet")
        .def(py::init<>())
        .def("__len__",[](FastSet* self){return std::distance(self->begin(), self->end());})
        .def("__contains__",[](FastSet* self, size_t key){return std::find(self->begin(), self->end(), key) != self->end();}, gtwrap::internal::py_arg<size_t>("key"))
        .def("__iter__",[](FastSet* self){return py::make_iterator(self->begin(), self->end());});

    py::class_<HessianFactor, gtsam::GaussianFactor, std::shared_ptr<HessianFactor>>(m_, "HessianFactor")
        .def(py::init<const gtsam::KeyVector&, const std::vector<gtsam::Matrix>&, const std::vector<gtsam::Vector>&, double>(), gtwrap::internal::py_arg<const gtsam::KeyVector&>("js"), gtwrap::internal::py_arg<const std::vector<gtsam::Matrix>&>("Gs"), gtwrap::internal::py_arg<const std::vector<gtsam::Vector>&>("gs"), gtwrap::internal::py_arg<double>("f"));

    py::class_<SmartProjectionRigFactor<gtsam::PinholeCamera<gtsam::Cal3_S2>>, gtsam::SmartProjectionFactor<gtsam::PinholeCamera<gtsam::Cal3_S2>>, std::shared_ptr<SmartProjectionRigFactor<gtsam::PinholeCamera<gtsam::Cal3_S2>>>>(m_, "SmartProjectionRigFactorPinholeCameraCal3_S2")
        .def("add",&gtwrap_generated_adapters::callable_36, gtwrap::internal::py_arg<const gtsam::PinholeCamera<gtsam::Cal3_S2>::Measurement&>("measured"), gtwrap::internal::py_arg<const gtsam::Key&>("poseKey"), gtwrap::internal::py_arg<const size_t&>("cameraId") = 0);

    py::class_<MyFactor<gtsam::Pose2, gtsam::Matrix>, std::shared_ptr<MyFactor<gtsam::Pose2, gtsam::Matrix>>>(m_, "MyFactorPosePoint2")
        .def(py::init<size_t, size_t, double, const std::shared_ptr<gtsam::noiseModel::Base>>(), gtwrap::internal::py_arg<size_t>("key1"), gtwrap::internal::py_arg<size_t>("key2"), gtwrap::internal::py_arg<double>("measured"), gtwrap::internal::py_arg<const std::shared_ptr<gtsam::noiseModel::Base>>("noiseModel"))
        .def("print",[](MyFactor<gtsam::Pose2, gtsam::Matrix>* self, const string& s, const gtsam::KeyFormatter& keyFormatter){ py::scoped_ostream_redirect output; self->print(s, keyFormatter);}, gtwrap::internal::py_arg<const string&>("s") = "factor: ", gtwrap::internal::py_arg<const gtsam::KeyFormatter&>("keyFormatter") = gtsam::DefaultKeyFormatter)
        .def("__repr__",
                    [](const MyFactor<gtsam::Pose2, gtsam::Matrix>& self, const string& s, const gtsam::KeyFormatter& keyFormatter){
                        gtsam::RedirectCout redirect;
                        self.print(s, keyFormatter);
                        return redirect.str();
                    }, gtwrap::internal::py_arg<const string&>("s") = "factor: ", gtwrap::internal::py_arg<const gtsam::KeyFormatter&>("keyFormatter") = gtsam::DefaultKeyFormatter);

    py::class_<SuperCoolFactor<gtsam::Pose3>, std::shared_ptr<SuperCoolFactor<gtsam::Pose3>>>(m_, "SuperCoolFactorPose3");

#include "python/specializations.h"

}

