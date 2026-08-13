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

PYBIND11_MODULE(inheritance_py, m_) {
    m_.doc() = "pybind11 wrapper of inheritance_py";


    // Named adapters avoid a unique callable type per binding.
    struct gtwrap_generated_adapters {
        static auto callable_0(MyTemplate<gtsam::Point2>* self, const gtsam::Point2& t) -> std::decay<decltype(self->templatedMethod<gtsam::Point2>(t))>::type { return self->templatedMethod<gtsam::Point2>(t); }
        static auto callable_1(MyTemplate<gtsam::Point2>* self, const gtsam::Point3& t) -> std::decay<decltype(self->templatedMethod<gtsam::Point3>(t))>::type { return self->templatedMethod<gtsam::Point3>(t); }
        static auto callable_2(MyTemplate<gtsam::Point2>* self, const gtsam::Vector& t) -> std::decay<decltype(self->templatedMethod<gtsam::Vector>(t))>::type { return self->templatedMethod<gtsam::Vector>(t); }
        static auto callable_3(MyTemplate<gtsam::Point2>* self, const gtsam::Matrix& t) -> std::decay<decltype(self->templatedMethod<gtsam::Matrix>(t))>::type { return self->templatedMethod<gtsam::Matrix>(t); }
        static void callable_4(MyTemplate<gtsam::Point2>* self, const gtsam::Point2& value) { self->accept_T(value); }
        static void callable_5(MyTemplate<gtsam::Point2>* self, std::shared_ptr<gtsam::Point2> value) { self->accept_Tptr(value); }
        static auto callable_6(MyTemplate<gtsam::Point2>* self, std::shared_ptr<gtsam::Point2> value) -> std::decay<decltype(self->return_Tptr(value))>::type { return self->return_Tptr(value); }
        static auto callable_7(MyTemplate<gtsam::Point2>* self, gtsam::Point2* value) -> std::decay<decltype(self->return_T(value))>::type { return self->return_T(value); }
        static auto callable_8(MyTemplate<gtsam::Point2>* self) -> std::decay<decltype(self->create_ptrs())>::type { return self->create_ptrs(); }
        static auto callable_9(MyTemplate<gtsam::Point2>* self) -> std::decay<decltype(self->create_MixedPtrs())>::type { return self->create_MixedPtrs(); }
        static auto callable_10(MyTemplate<gtsam::Point2>* self, std::shared_ptr<gtsam::Point2> p1, std::shared_ptr<gtsam::Point2> p2) -> std::decay<decltype(self->return_ptrs(p1, p2))>::type { return self->return_ptrs(p1, p2); }
        static auto callable_11(const gtsam::Point2& K) -> std::decay<decltype(MyTemplate<gtsam::Point2>::Level(K))>::type { return MyTemplate<gtsam::Point2>::Level(K); }
        static auto callable_12(MyTemplate<gtsam::Matrix>* self, const gtsam::Point2& t) -> std::decay<decltype(self->templatedMethod<gtsam::Point2>(t))>::type { return self->templatedMethod<gtsam::Point2>(t); }
        static auto callable_13(MyTemplate<gtsam::Matrix>* self, const gtsam::Point3& t) -> std::decay<decltype(self->templatedMethod<gtsam::Point3>(t))>::type { return self->templatedMethod<gtsam::Point3>(t); }
        static auto callable_14(MyTemplate<gtsam::Matrix>* self, const gtsam::Vector& t) -> std::decay<decltype(self->templatedMethod<gtsam::Vector>(t))>::type { return self->templatedMethod<gtsam::Vector>(t); }
        static auto callable_15(MyTemplate<gtsam::Matrix>* self, const gtsam::Matrix& t) -> std::decay<decltype(self->templatedMethod<gtsam::Matrix>(t))>::type { return self->templatedMethod<gtsam::Matrix>(t); }
        static void callable_16(MyTemplate<gtsam::Matrix>* self, const gtsam::Matrix& value) { self->accept_T(value); }
        static void callable_17(MyTemplate<gtsam::Matrix>* self, std::shared_ptr<gtsam::Matrix> value) { self->accept_Tptr(value); }
        static auto callable_18(MyTemplate<gtsam::Matrix>* self, std::shared_ptr<gtsam::Matrix> value) -> std::decay<decltype(self->return_Tptr(value))>::type { return self->return_Tptr(value); }
        static auto callable_19(MyTemplate<gtsam::Matrix>* self, gtsam::Matrix* value) -> std::decay<decltype(self->return_T(value))>::type { return self->return_T(value); }
        static auto callable_20(MyTemplate<gtsam::Matrix>* self) -> std::decay<decltype(self->create_ptrs())>::type { return self->create_ptrs(); }
        static auto callable_21(MyTemplate<gtsam::Matrix>* self) -> std::decay<decltype(self->create_MixedPtrs())>::type { return self->create_MixedPtrs(); }
        static auto callable_22(MyTemplate<gtsam::Matrix>* self, std::shared_ptr<gtsam::Matrix> p1, std::shared_ptr<gtsam::Matrix> p2) -> std::decay<decltype(self->return_ptrs(p1, p2))>::type { return self->return_ptrs(p1, p2); }
        static auto callable_23(const gtsam::Matrix& K) -> std::decay<decltype(MyTemplate<gtsam::Matrix>::Level(K))>::type { return MyTemplate<gtsam::Matrix>::Level(K); }
        static auto callable_24(MyTemplate<A>* self, const gtsam::Point2& t) -> std::decay<decltype(self->templatedMethod<gtsam::Point2>(t))>::type { return self->templatedMethod<gtsam::Point2>(t); }
        static auto callable_25(MyTemplate<A>* self, const gtsam::Point3& t) -> std::decay<decltype(self->templatedMethod<gtsam::Point3>(t))>::type { return self->templatedMethod<gtsam::Point3>(t); }
        static auto callable_26(MyTemplate<A>* self, const gtsam::Vector& t) -> std::decay<decltype(self->templatedMethod<gtsam::Vector>(t))>::type { return self->templatedMethod<gtsam::Vector>(t); }
        static auto callable_27(MyTemplate<A>* self, const gtsam::Matrix& t) -> std::decay<decltype(self->templatedMethod<gtsam::Matrix>(t))>::type { return self->templatedMethod<gtsam::Matrix>(t); }
        static void callable_28(MyTemplate<A>* self, const A& value) { self->accept_T(value); }
        static void callable_29(MyTemplate<A>* self, std::shared_ptr<A> value) { self->accept_Tptr(value); }
        static auto callable_30(MyTemplate<A>* self, std::shared_ptr<A> value) -> std::decay<decltype(self->return_Tptr(value))>::type { return self->return_Tptr(value); }
        static auto callable_31(MyTemplate<A>* self, A* value) -> std::decay<decltype(self->return_T(value))>::type { return self->return_T(value); }
        static auto callable_32(MyTemplate<A>* self) -> std::decay<decltype(self->create_ptrs())>::type { return self->create_ptrs(); }
        static auto callable_33(MyTemplate<A>* self) -> std::decay<decltype(self->create_MixedPtrs())>::type { return self->create_MixedPtrs(); }
        static auto callable_34(MyTemplate<A>* self, std::shared_ptr<A> p1, std::shared_ptr<A> p2) -> std::decay<decltype(self->return_ptrs(p1, p2))>::type { return self->return_ptrs(p1, p2); }
        static auto callable_35(const A& K) -> std::decay<decltype(MyTemplate<A>::Level(K))>::type { return MyTemplate<A>::Level(K); }
        static auto callable_36(double x) -> std::decay<decltype(Base::Create(x))>::type { return Base::Create(x); }
    };

    py::class_<MyBase, std::shared_ptr<MyBase>>(m_, "MyBase");

    py::class_<MyTemplate<gtsam::Point2>, MyBase, std::shared_ptr<MyTemplate<gtsam::Point2>>>(m_, "MyTemplatePoint2")
        .def(py::init<>())
        .def("templatedMethodPoint2",&gtwrap_generated_adapters::callable_0, gtwrap::internal::py_arg<const gtsam::Point2&>("t"))
        .def("templatedMethodPoint3",&gtwrap_generated_adapters::callable_1, gtwrap::internal::py_arg<const gtsam::Point3&>("t"))
        .def("templatedMethodVector",&gtwrap_generated_adapters::callable_2, gtwrap::internal::py_arg<const gtsam::Vector&>("t"))
        .def("templatedMethodMatrix",&gtwrap_generated_adapters::callable_3, gtwrap::internal::py_arg<const gtsam::Matrix&>("t"))
        .def("accept_T",&gtwrap_generated_adapters::callable_4, gtwrap::internal::py_arg<const gtsam::Point2&>("value"))
        .def("accept_Tptr",&gtwrap_generated_adapters::callable_5, gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("value"))
        .def("return_Tptr",&gtwrap_generated_adapters::callable_6, gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("value"))
        .def("return_T",&gtwrap_generated_adapters::callable_7, gtwrap::internal::py_arg<gtsam::Point2*>("value"))
        .def("create_ptrs",&gtwrap_generated_adapters::callable_8)
        .def("create_MixedPtrs",&gtwrap_generated_adapters::callable_9)
        .def("return_ptrs",&gtwrap_generated_adapters::callable_10, gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("p2"))
        .def_static("Level",&gtwrap_generated_adapters::callable_11, gtwrap::internal::py_arg<const gtsam::Point2&>("K"));

    py::class_<MyTemplate<gtsam::Matrix>, MyBase, std::shared_ptr<MyTemplate<gtsam::Matrix>>>(m_, "MyTemplateMatrix")
        .def(py::init<>())
        .def("templatedMethodPoint2",&gtwrap_generated_adapters::callable_12, gtwrap::internal::py_arg<const gtsam::Point2&>("t"))
        .def("templatedMethodPoint3",&gtwrap_generated_adapters::callable_13, gtwrap::internal::py_arg<const gtsam::Point3&>("t"))
        .def("templatedMethodVector",&gtwrap_generated_adapters::callable_14, gtwrap::internal::py_arg<const gtsam::Vector&>("t"))
        .def("templatedMethodMatrix",&gtwrap_generated_adapters::callable_15, gtwrap::internal::py_arg<const gtsam::Matrix&>("t"))
        .def("accept_T",&gtwrap_generated_adapters::callable_16, gtwrap::internal::py_arg<const gtsam::Matrix&>("value"))
        .def("accept_Tptr",&gtwrap_generated_adapters::callable_17, gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("value"))
        .def("return_Tptr",&gtwrap_generated_adapters::callable_18, gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("value"))
        .def("return_T",&gtwrap_generated_adapters::callable_19, gtwrap::internal::py_arg<gtsam::Matrix*>("value"))
        .def("create_ptrs",&gtwrap_generated_adapters::callable_20)
        .def("create_MixedPtrs",&gtwrap_generated_adapters::callable_21)
        .def("return_ptrs",&gtwrap_generated_adapters::callable_22, gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("p2"))
        .def_static("Level",&gtwrap_generated_adapters::callable_23, gtwrap::internal::py_arg<const gtsam::Matrix&>("K"));

    py::class_<MyTemplate<A>, MyBase, std::shared_ptr<MyTemplate<A>>>(m_, "MyTemplateA")
        .def(py::init<>())
        .def("templatedMethodPoint2",&gtwrap_generated_adapters::callable_24, gtwrap::internal::py_arg<const gtsam::Point2&>("t"))
        .def("templatedMethodPoint3",&gtwrap_generated_adapters::callable_25, gtwrap::internal::py_arg<const gtsam::Point3&>("t"))
        .def("templatedMethodVector",&gtwrap_generated_adapters::callable_26, gtwrap::internal::py_arg<const gtsam::Vector&>("t"))
        .def("templatedMethodMatrix",&gtwrap_generated_adapters::callable_27, gtwrap::internal::py_arg<const gtsam::Matrix&>("t"))
        .def("accept_T",&gtwrap_generated_adapters::callable_28, gtwrap::internal::py_arg<const A&>("value"))
        .def("accept_Tptr",&gtwrap_generated_adapters::callable_29, gtwrap::internal::py_arg<std::shared_ptr<A>>("value"))
        .def("return_Tptr",&gtwrap_generated_adapters::callable_30, gtwrap::internal::py_arg<std::shared_ptr<A>>("value"))
        .def("return_T",&gtwrap_generated_adapters::callable_31, gtwrap::internal::py_arg<A*>("value"))
        .def("create_ptrs",&gtwrap_generated_adapters::callable_32)
        .def("create_MixedPtrs",&gtwrap_generated_adapters::callable_33)
        .def("return_ptrs",&gtwrap_generated_adapters::callable_34, gtwrap::internal::py_arg<std::shared_ptr<A>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<A>>("p2"))
        .def_static("Level",&gtwrap_generated_adapters::callable_35, gtwrap::internal::py_arg<const A&>("K"));

    py::class_<ForwardKinematicsFactor, gtsam::BetweenFactor<gtsam::Pose3>, std::shared_ptr<ForwardKinematicsFactor>>(m_, "ForwardKinematicsFactor");

    py::class_<ParentHasTemplate<double>, MyTemplate<double>, std::shared_ptr<ParentHasTemplate<double>>>(m_, "ParentHasTemplateDouble");

    py::class_<Base, std::shared_ptr<Base>>(m_, "Base")
        .def_static("Create",&gtwrap_generated_adapters::callable_36, gtwrap::internal::py_arg<double>("x"));

    py::class_<Derived, Base, std::shared_ptr<Derived>>(m_, "Derived");


#include "python/specializations.h"

}

