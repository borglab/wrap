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

PYBIND11_MODULE(functions_py, m_) {
    m_.doc() = "pybind11 wrapper of functions_py";


    // Named adapters avoid a unique callable type per binding.
    struct gtwrap_generated_adapters {
        static auto callable_0(string filename, std::shared_ptr<Test> model, int maxID, bool addNoise, bool smart) -> std::decay<decltype(::load2D(filename, model, maxID, addNoise, smart))>::type { return ::load2D(filename, model, maxID, addNoise, smart); }
        static auto callable_1(string filename, const std::shared_ptr<gtsam::noiseModel::Diagonal> model, int maxID, bool addNoise, bool smart) -> std::decay<decltype(::load2D(filename, model, maxID, addNoise, smart))>::type { return ::load2D(filename, model, maxID, addNoise, smart); }
        static auto callable_2(string filename, gtsam::noiseModel::Diagonal* model) -> std::decay<decltype(::load2D(filename, model))>::type { return ::load2D(filename, model); }
        static auto callable_3() -> std::decay<decltype(::aGlobalFunction())>::type { return ::aGlobalFunction(); }
        static auto callable_4(int a) -> std::decay<decltype(::overloadedGlobalFunction(a))>::type { return ::overloadedGlobalFunction(a); }
        static auto callable_5(int a, double b) -> std::decay<decltype(::overloadedGlobalFunction(a, b))>::type { return ::overloadedGlobalFunction(a, b); }
        static auto callable_6(const string& x, size_t y) -> std::decay<decltype(::MultiTemplatedFunction<string,size_t,double>(x, y))>::type { return ::MultiTemplatedFunction<string,size_t,double>(x, y); }
        static auto callable_7(const double& x, size_t y) -> std::decay<decltype(::MultiTemplatedFunction<double,size_t,double>(x, y))>::type { return ::MultiTemplatedFunction<double,size_t,double>(x, y); }
        static void callable_8(int a, int b) { ::DefaultFuncInt(a, b); }
        static void callable_9(const string& s, const string& name) { ::DefaultFuncString(s, name); }
        static void callable_10(const gtsam::KeyFormatter& keyFormatter) { ::DefaultFuncObj(keyFormatter); }
        static void callable_11(int a, int b, double c, int d, bool e) { ::DefaultFuncZero(a, b, c, d, e); }
        static void callable_12(const std::vector<int>& i, const std::vector<string>& s) { ::DefaultFuncVector(i, s); }
        static void callable_13(const gtsam::Pose3& pose) { ::setPose(pose); }
        static auto callable_14(const gtsam::DiscreteFactorGraph& factors, const gtsam::Ordering& frontalKeys) -> std::decay<decltype(::EliminateDiscrete(factors, frontalKeys))>::type { return ::EliminateDiscrete(factors, frontalKeys); }
        static auto callable_15(const gtsam::Pose3Vector& poses, std::shared_ptr<gtsam::Cal3_S2> sharedCal, const gtsam::Point2Vector& measurements, double rank_tol, bool optimize, const gtsam::SharedNoiseModel& model) -> std::decay<decltype(::triangulatePoint3<gtsam::Cal3_S2>(poses, sharedCal, measurements, rank_tol, optimize, model))>::type { return ::triangulatePoint3<gtsam::Cal3_S2>(poses, sharedCal, measurements, rank_tol, optimize, model); }
        static auto callable_16(const std::vector<gtsam::Point3>& elements) -> std::decay<decltype(::FindKarcherMean<gtsam::Point3>(elements))>::type { return ::FindKarcherMean<gtsam::Point3>(elements); }
        static auto callable_17(const std::vector<gtsam::SO3>& elements) -> std::decay<decltype(::FindKarcherMean<gtsam::SO3>(elements))>::type { return ::FindKarcherMean<gtsam::SO3>(elements); }
        static auto callable_18(const std::vector<gtsam::SO4>& elements) -> std::decay<decltype(::FindKarcherMean<gtsam::SO4>(elements))>::type { return ::FindKarcherMean<gtsam::SO4>(elements); }
        static auto callable_19(const std::vector<gtsam::Pose3>& elements) -> std::decay<decltype(::FindKarcherMean<gtsam::Pose3>(elements))>::type { return ::FindKarcherMean<gtsam::Pose3>(elements); }
        static void callable_20(const gtsam::Rot3& t) { ::TemplatedFunction<gtsam::Rot3>(t); }
    };

    m_.def("load2D",&gtwrap_generated_adapters::callable_0, gtwrap::internal::py_arg<string>("filename"), gtwrap::internal::py_arg<std::shared_ptr<Test>>("model"), gtwrap::internal::py_arg<int>("maxID"), gtwrap::internal::py_arg<bool>("addNoise"), gtwrap::internal::py_arg<bool>("smart"));
    m_.def("load2D",&gtwrap_generated_adapters::callable_1, gtwrap::internal::py_arg<string>("filename"), gtwrap::internal::py_arg<const std::shared_ptr<gtsam::noiseModel::Diagonal>>("model"), gtwrap::internal::py_arg<int>("maxID"), gtwrap::internal::py_arg<bool>("addNoise"), gtwrap::internal::py_arg<bool>("smart"));
    m_.def("load2D",&gtwrap_generated_adapters::callable_2, gtwrap::internal::py_arg<string>("filename"), gtwrap::internal::py_arg<gtsam::noiseModel::Diagonal*>("model"));
    m_.def("aGlobalFunction",&gtwrap_generated_adapters::callable_3);
    m_.def("overloadedGlobalFunction",&gtwrap_generated_adapters::callable_4, gtwrap::internal::py_arg<int>("a"));
    m_.def("overloadedGlobalFunction",&gtwrap_generated_adapters::callable_5, gtwrap::internal::py_arg<int>("a"), gtwrap::internal::py_arg<double>("b"));
    m_.def("MultiTemplatedFunctionStringSize_tDouble",&gtwrap_generated_adapters::callable_6, gtwrap::internal::py_arg<const string&>("x"), gtwrap::internal::py_arg<size_t>("y"));
    m_.def("MultiTemplatedFunctionDoubleSize_tDouble",&gtwrap_generated_adapters::callable_7, gtwrap::internal::py_arg<const double&>("x"), gtwrap::internal::py_arg<size_t>("y"));
    m_.def("DefaultFuncInt",&gtwrap_generated_adapters::callable_8, gtwrap::internal::py_arg<int>("a") = 123, gtwrap::internal::py_arg<int>("b") = 0);
    m_.def("DefaultFuncString",&gtwrap_generated_adapters::callable_9, gtwrap::internal::py_arg<const string&>("s") = "hello", gtwrap::internal::py_arg<const string&>("name") = "");
    m_.def("DefaultFuncObj",&gtwrap_generated_adapters::callable_10, gtwrap::internal::py_arg<const gtsam::KeyFormatter&>("keyFormatter") = gtsam::DefaultKeyFormatter);
    m_.def("DefaultFuncZero",&gtwrap_generated_adapters::callable_11, gtwrap::internal::py_arg<int>("a"), gtwrap::internal::py_arg<int>("b"), gtwrap::internal::py_arg<double>("c") = 0.0, gtwrap::internal::py_arg<int>("d") = 0, gtwrap::internal::py_arg<bool>("e") = false);
    m_.def("DefaultFuncVector",&gtwrap_generated_adapters::callable_12, gtwrap::internal::py_arg<const std::vector<int>&>("i") = {1, 2, 3}, gtwrap::internal::py_arg<const std::vector<string>&>("s") = {"borglab", "gtsam"});
    m_.def("setPose",&gtwrap_generated_adapters::callable_13, gtwrap::internal::py_arg<const gtsam::Pose3&>("pose") = gtsam::Pose3());
    m_.def("EliminateDiscrete",&gtwrap_generated_adapters::callable_14, gtwrap::internal::py_arg<const gtsam::DiscreteFactorGraph&>("factors"), gtwrap::internal::py_arg<const gtsam::Ordering&>("frontalKeys"));
    m_.def("triangulatePoint3Cal3_S2",&gtwrap_generated_adapters::callable_15, gtwrap::internal::py_arg<const gtsam::Pose3Vector&>("poses"), gtwrap::internal::py_arg<std::shared_ptr<gtsam::Cal3_S2>>("sharedCal"), gtwrap::internal::py_arg<const gtsam::Point2Vector&>("measurements"), gtwrap::internal::py_arg<double>("rank_tol"), gtwrap::internal::py_arg<bool>("optimize"), gtwrap::internal::py_arg<const gtsam::SharedNoiseModel&>("model") = nullptr);
    m_.def("FindKarcherMeanPoint3",&gtwrap_generated_adapters::callable_16, gtwrap::internal::py_arg<const std::vector<gtsam::Point3>&>("elements"));
    m_.def("FindKarcherMeanSO3",&gtwrap_generated_adapters::callable_17, gtwrap::internal::py_arg<const std::vector<gtsam::SO3>&>("elements"));
    m_.def("FindKarcherMeanSO4",&gtwrap_generated_adapters::callable_18, gtwrap::internal::py_arg<const std::vector<gtsam::SO4>&>("elements"));
    m_.def("FindKarcherMeanPose3",&gtwrap_generated_adapters::callable_19, gtwrap::internal::py_arg<const std::vector<gtsam::Pose3>&>("elements"));
    m_.def("TemplatedFunctionRot3",&gtwrap_generated_adapters::callable_20, gtwrap::internal::py_arg<const gtsam::Rot3&>("t"));

#include "python/specializations.h"

}

