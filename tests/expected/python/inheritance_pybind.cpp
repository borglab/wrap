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

PYBIND11_MODULE(inheritance_py, m_) {
    m_.doc() = "pybind11 wrapper of inheritance_py";


    py::class_<MyBase, std::shared_ptr<MyBase>>(m_, "MyBase");

    py::class_<MyTemplate<gtsam::Point2>, MyBase, std::shared_ptr<MyTemplate<gtsam::Point2>>>(m_, "MyTemplatePoint2")
        .def(py::init<>())
        .def("templatedMethodPoint2",gtwrap::internal::SelectOverload<const gtsam::Point2&>::method(&MyTemplate<gtsam::Point2>::templatedMethod<gtsam::Point2>), gtwrap::internal::py_arg<const gtsam::Point2&>("t"))
        .def("templatedMethodPoint3",gtwrap::internal::SelectOverload<const gtsam::Point3&>::method(&MyTemplate<gtsam::Point2>::templatedMethod<gtsam::Point3>), gtwrap::internal::py_arg<const gtsam::Point3&>("t"))
        .def("templatedMethodVector",gtwrap::internal::SelectOverload<const gtsam::Vector&>::method(&MyTemplate<gtsam::Point2>::templatedMethod<gtsam::Vector>), gtwrap::internal::py_arg<const gtsam::Vector&>("t"))
        .def("templatedMethodMatrix",gtwrap::internal::SelectOverload<const gtsam::Matrix&>::method(&MyTemplate<gtsam::Point2>::templatedMethod<gtsam::Matrix>), gtwrap::internal::py_arg<const gtsam::Matrix&>("t"))
        .def("accept_T",gtwrap::internal::SelectOverload<const gtsam::Point2&>::const_method(&MyTemplate<gtsam::Point2>::accept_T), gtwrap::internal::py_arg<const gtsam::Point2&>("value"))
        .def("accept_Tptr",gtwrap::internal::SelectOverload<std::shared_ptr<gtsam::Point2>>::const_method(&MyTemplate<gtsam::Point2>::accept_Tptr), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("value"))
        .def("return_Tptr",gtwrap::internal::SelectOverload<std::shared_ptr<gtsam::Point2>>::const_method(&MyTemplate<gtsam::Point2>::return_Tptr), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("value"))
        .def("return_T",gtwrap::internal::SelectOverload<gtsam::Point2*>::const_method(&MyTemplate<gtsam::Point2>::return_T), gtwrap::internal::py_arg<gtsam::Point2*>("value"))
        .def("create_ptrs",gtwrap::internal::SelectOverload<>::const_method(&MyTemplate<gtsam::Point2>::create_ptrs))
        .def("create_MixedPtrs",gtwrap::internal::SelectOverload<>::const_method(&MyTemplate<gtsam::Point2>::create_MixedPtrs))
        .def("return_ptrs",gtwrap::internal::SelectOverload<std::shared_ptr<gtsam::Point2>, std::shared_ptr<gtsam::Point2>>::const_method(&MyTemplate<gtsam::Point2>::return_ptrs), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Point2>>("p2"))
        .def_static("Level",gtwrap::internal::SelectOverload<const gtsam::Point2&>::function(&MyTemplate<gtsam::Point2>::Level), gtwrap::internal::py_arg<const gtsam::Point2&>("K"));

    py::class_<MyTemplate<gtsam::Matrix>, MyBase, std::shared_ptr<MyTemplate<gtsam::Matrix>>>(m_, "MyTemplateMatrix")
        .def(py::init<>())
        .def("templatedMethodPoint2",gtwrap::internal::SelectOverload<const gtsam::Point2&>::method(&MyTemplate<gtsam::Matrix>::templatedMethod<gtsam::Point2>), gtwrap::internal::py_arg<const gtsam::Point2&>("t"))
        .def("templatedMethodPoint3",gtwrap::internal::SelectOverload<const gtsam::Point3&>::method(&MyTemplate<gtsam::Matrix>::templatedMethod<gtsam::Point3>), gtwrap::internal::py_arg<const gtsam::Point3&>("t"))
        .def("templatedMethodVector",gtwrap::internal::SelectOverload<const gtsam::Vector&>::method(&MyTemplate<gtsam::Matrix>::templatedMethod<gtsam::Vector>), gtwrap::internal::py_arg<const gtsam::Vector&>("t"))
        .def("templatedMethodMatrix",gtwrap::internal::SelectOverload<const gtsam::Matrix&>::method(&MyTemplate<gtsam::Matrix>::templatedMethod<gtsam::Matrix>), gtwrap::internal::py_arg<const gtsam::Matrix&>("t"))
        .def("accept_T",gtwrap::internal::SelectOverload<const gtsam::Matrix&>::const_method(&MyTemplate<gtsam::Matrix>::accept_T), gtwrap::internal::py_arg<const gtsam::Matrix&>("value"))
        .def("accept_Tptr",gtwrap::internal::SelectOverload<std::shared_ptr<gtsam::Matrix>>::const_method(&MyTemplate<gtsam::Matrix>::accept_Tptr), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("value"))
        .def("return_Tptr",gtwrap::internal::SelectOverload<std::shared_ptr<gtsam::Matrix>>::const_method(&MyTemplate<gtsam::Matrix>::return_Tptr), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("value"))
        .def("return_T",gtwrap::internal::SelectOverload<gtsam::Matrix*>::const_method(&MyTemplate<gtsam::Matrix>::return_T), gtwrap::internal::py_arg<gtsam::Matrix*>("value"))
        .def("create_ptrs",gtwrap::internal::SelectOverload<>::const_method(&MyTemplate<gtsam::Matrix>::create_ptrs))
        .def("create_MixedPtrs",gtwrap::internal::SelectOverload<>::const_method(&MyTemplate<gtsam::Matrix>::create_MixedPtrs))
        .def("return_ptrs",gtwrap::internal::SelectOverload<std::shared_ptr<gtsam::Matrix>, std::shared_ptr<gtsam::Matrix>>::const_method(&MyTemplate<gtsam::Matrix>::return_ptrs), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Matrix>>("p2"))
        .def_static("Level",gtwrap::internal::SelectOverload<const gtsam::Matrix&>::function(&MyTemplate<gtsam::Matrix>::Level), gtwrap::internal::py_arg<const gtsam::Matrix&>("K"));

    py::class_<MyTemplate<A>, MyBase, std::shared_ptr<MyTemplate<A>>>(m_, "MyTemplateA")
        .def(py::init<>())
        .def("templatedMethodPoint2",gtwrap::internal::SelectOverload<const gtsam::Point2&>::method(&MyTemplate<A>::templatedMethod<gtsam::Point2>), gtwrap::internal::py_arg<const gtsam::Point2&>("t"))
        .def("templatedMethodPoint3",gtwrap::internal::SelectOverload<const gtsam::Point3&>::method(&MyTemplate<A>::templatedMethod<gtsam::Point3>), gtwrap::internal::py_arg<const gtsam::Point3&>("t"))
        .def("templatedMethodVector",gtwrap::internal::SelectOverload<const gtsam::Vector&>::method(&MyTemplate<A>::templatedMethod<gtsam::Vector>), gtwrap::internal::py_arg<const gtsam::Vector&>("t"))
        .def("templatedMethodMatrix",gtwrap::internal::SelectOverload<const gtsam::Matrix&>::method(&MyTemplate<A>::templatedMethod<gtsam::Matrix>), gtwrap::internal::py_arg<const gtsam::Matrix&>("t"))
        .def("accept_T",gtwrap::internal::SelectOverload<const A&>::const_method(&MyTemplate<A>::accept_T), gtwrap::internal::py_arg<const A&>("value"))
        .def("accept_Tptr",gtwrap::internal::SelectOverload<std::shared_ptr<A>>::const_method(&MyTemplate<A>::accept_Tptr), gtwrap::internal::py_arg<std::shared_ptr<A>>("value"))
        .def("return_Tptr",gtwrap::internal::SelectOverload<std::shared_ptr<A>>::const_method(&MyTemplate<A>::return_Tptr), gtwrap::internal::py_arg<std::shared_ptr<A>>("value"))
        .def("return_T",gtwrap::internal::SelectOverload<A*>::const_method(&MyTemplate<A>::return_T), gtwrap::internal::py_arg<A*>("value"))
        .def("create_ptrs",gtwrap::internal::SelectOverload<>::const_method(&MyTemplate<A>::create_ptrs))
        .def("create_MixedPtrs",gtwrap::internal::SelectOverload<>::const_method(&MyTemplate<A>::create_MixedPtrs))
        .def("return_ptrs",gtwrap::internal::SelectOverload<std::shared_ptr<A>, std::shared_ptr<A>>::const_method(&MyTemplate<A>::return_ptrs), gtwrap::internal::py_arg<std::shared_ptr<A>>("p1"), gtwrap::internal::py_arg<std::shared_ptr<A>>("p2"))
        .def_static("Level",gtwrap::internal::SelectOverload<const A&>::function(&MyTemplate<A>::Level), gtwrap::internal::py_arg<const A&>("K"));

    py::class_<ForwardKinematicsFactor, gtsam::BetweenFactor<gtsam::Pose3>, std::shared_ptr<ForwardKinematicsFactor>>(m_, "ForwardKinematicsFactor");

    py::class_<ParentHasTemplate<double>, MyTemplate<double>, std::shared_ptr<ParentHasTemplate<double>>>(m_, "ParentHasTemplateDouble");

    py::class_<Base, std::shared_ptr<Base>>(m_, "Base")
        .def_static("Create",gtwrap::internal::SelectOverload<double>::function(&Base::Create), gtwrap::internal::py_arg<double>("x"));

    py::class_<Derived, Base, std::shared_ptr<Derived>>(m_, "Derived");


#include "python/specializations.h"

}

