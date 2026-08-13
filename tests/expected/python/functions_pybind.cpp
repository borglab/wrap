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

PYBIND11_MODULE(functions_py, m_) {
    m_.doc() = "pybind11 wrapper of functions_py";


    m_.def("load2D",gtwrap::internal::SelectOverload<string, std::shared_ptr<Test>, int, bool, bool>::function(&::load2D), gtwrap::internal::py_arg<string>("filename"), gtwrap::internal::py_arg<std::shared_ptr<Test>>("model"), gtwrap::internal::py_arg<int>("maxID"), gtwrap::internal::py_arg<bool>("addNoise"), gtwrap::internal::py_arg<bool>("smart"));
    m_.def("load2D",gtwrap::internal::SelectOverload<string, const std::shared_ptr<gtsam::noiseModel::Diagonal>, int, bool, bool>::function(&::load2D), gtwrap::internal::py_arg<string>("filename"), gtwrap::internal::py_arg<const std::shared_ptr<gtsam::noiseModel::Diagonal>>("model"), gtwrap::internal::py_arg<int>("maxID"), gtwrap::internal::py_arg<bool>("addNoise"), gtwrap::internal::py_arg<bool>("smart"));
    m_.def("load2D",gtwrap::internal::SelectOverload<string, gtsam::noiseModel::Diagonal*>::function(&::load2D), gtwrap::internal::py_arg<string>("filename"), gtwrap::internal::py_arg<gtsam::noiseModel::Diagonal*>("model"));
    m_.def("aGlobalFunction",gtwrap::internal::SelectOverload<>::function(&::aGlobalFunction));
    m_.def("overloadedGlobalFunction",gtwrap::internal::SelectOverload<int>::function(&::overloadedGlobalFunction), gtwrap::internal::py_arg<int>("a"));
    m_.def("overloadedGlobalFunction",gtwrap::internal::SelectOverload<int, double>::function(&::overloadedGlobalFunction), gtwrap::internal::py_arg<int>("a"), gtwrap::internal::py_arg<double>("b"));
    m_.def("MultiTemplatedFunctionStringSize_tDouble",gtwrap::internal::SelectOverload<const string&, size_t>::function(&::MultiTemplatedFunction<string,size_t,double>), gtwrap::internal::py_arg<const string&>("x"), gtwrap::internal::py_arg<size_t>("y"));
    m_.def("MultiTemplatedFunctionDoubleSize_tDouble",gtwrap::internal::SelectOverload<const double&, size_t>::function(&::MultiTemplatedFunction<double,size_t,double>), gtwrap::internal::py_arg<const double&>("x"), gtwrap::internal::py_arg<size_t>("y"));
    m_.def("DefaultFuncInt",gtwrap::internal::SelectOverload<int, int>::function(&::DefaultFuncInt), gtwrap::internal::py_arg<int>("a") = 123, gtwrap::internal::py_arg<int>("b") = 0);
    m_.def("DefaultFuncString",gtwrap::internal::SelectOverload<const string&, const string&>::function(&::DefaultFuncString), gtwrap::internal::py_arg<const string&>("s") = "hello", gtwrap::internal::py_arg<const string&>("name") = "");
    m_.def("DefaultFuncObj",gtwrap::internal::SelectOverload<const gtsam::KeyFormatter&>::function(&::DefaultFuncObj), gtwrap::internal::py_arg<const gtsam::KeyFormatter&>("keyFormatter") = gtsam::DefaultKeyFormatter);
    m_.def("DefaultFuncZero",gtwrap::internal::SelectOverload<int, int, double, int, bool>::function(&::DefaultFuncZero), gtwrap::internal::py_arg<int>("a"), gtwrap::internal::py_arg<int>("b"), gtwrap::internal::py_arg<double>("c") = 0.0, gtwrap::internal::py_arg<int>("d") = 0, gtwrap::internal::py_arg<bool>("e") = false);
    m_.def("DefaultFuncVector",gtwrap::internal::SelectOverload<const std::vector<int>&, const std::vector<string>&>::function(&::DefaultFuncVector), gtwrap::internal::py_arg<const std::vector<int>&>("i") = {1, 2, 3}, gtwrap::internal::py_arg<const std::vector<string>&>("s") = {"borglab", "gtsam"});
    m_.def("setPose",gtwrap::internal::SelectOverload<const gtsam::Pose3&>::function(&::setPose), gtwrap::internal::py_arg<const gtsam::Pose3&>("pose") = gtsam::Pose3());
    m_.def("EliminateDiscrete",gtwrap::internal::SelectOverload<const gtsam::DiscreteFactorGraph&, const gtsam::Ordering&>::function(&::EliminateDiscrete), gtwrap::internal::py_arg<const gtsam::DiscreteFactorGraph&>("factors"), gtwrap::internal::py_arg<const gtsam::Ordering&>("frontalKeys"));
    m_.def("triangulatePoint3Cal3_S2",gtwrap::internal::SelectOverload<const gtsam::Pose3Vector&, std::shared_ptr<gtsam::Cal3_S2>, const gtsam::Point2Vector&, double, bool, const gtsam::SharedNoiseModel&>::function(&::triangulatePoint3<gtsam::Cal3_S2>), gtwrap::internal::py_arg<const gtsam::Pose3Vector&>("poses"), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Cal3_S2>>("sharedCal"), gtwrap::internal::py_arg<const gtsam::Point2Vector&>("measurements"), gtwrap::internal::py_arg<double>("rank_tol"), gtwrap::internal::py_arg<bool>("optimize"), gtwrap::internal::py_arg<const gtsam::SharedNoiseModel&>("model") = nullptr);
    m_.def("FindKarcherMeanPoint3",gtwrap::internal::SelectOverload<const std::vector<gtsam::Point3>&>::function(&::FindKarcherMean<gtsam::Point3>), gtwrap::internal::py_arg<const std::vector<gtsam::Point3>&>("elements"));
    m_.def("FindKarcherMeanSO3",gtwrap::internal::SelectOverload<const std::vector<gtsam::SO3>&>::function(&::FindKarcherMean<gtsam::SO3>), gtwrap::internal::py_arg<const std::vector<gtsam::SO3>&>("elements"));
    m_.def("FindKarcherMeanSO4",gtwrap::internal::SelectOverload<const std::vector<gtsam::SO4>&>::function(&::FindKarcherMean<gtsam::SO4>), gtwrap::internal::py_arg<const std::vector<gtsam::SO4>&>("elements"));
    m_.def("FindKarcherMeanPose3",gtwrap::internal::SelectOverload<const std::vector<gtsam::Pose3>&>::function(&::FindKarcherMean<gtsam::Pose3>), gtwrap::internal::py_arg<const std::vector<gtsam::Pose3>&>("elements"));
    m_.def("TemplatedFunctionRot3",gtwrap::internal::SelectOverload<const gtsam::Rot3&>::function(&::TemplatedFunction<gtsam::Rot3>), gtwrap::internal::py_arg<const gtsam::Rot3&>("t"));

#include "python/specializations.h"

}

