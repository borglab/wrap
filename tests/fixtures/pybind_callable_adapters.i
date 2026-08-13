#include <pybind_callable_adapters.h>

namespace adapters {

class BaseAdapter {
  BaseAdapter();

  @pybind_adapter
  int inherited(int value) const;
};

template<T = {int}>
class Adapter: adapters::BaseAdapter {
  Adapter();

  int exact(int value);
  int exactConst(int value) const;
  static int exactStatic(int value);

  @pybind_adapter
  int omittedDefault(int value) const;

  @pybind_adapter
  int referenceArgument(int value) const;

  int hiddenOverload(int value) const;

  int declaredOverload(int value) const;
  double declaredOverload(double value) const;

  @pybind_adapter
  T at(size_t index) const;

  @pybind_adapter
  T front() const;

  @pybind_adapter
  int alias(int index) const;

  @pybind_adapter
  static int staticOmitted(int value);

  template<U = {double}>
  U exactTemplated(U value) const;

  template<U = {double}>
  @pybind_adapter
  U adaptedTemplated(U value) const;

  @pybind_adapter
  const string& lambda(const string& value = "fallback") const;
};

int exactGlobal(int value);

@pybind_adapter
int globalOmitted(int value);

int globalHidden(int value);

int globalOverload(int value);
double globalOverload(double value);

template<T = {int}>
T exactGlobalTemplated(T value);

template<T = {int}>
@pybind_adapter
T adaptedGlobalTemplated(T value);

}
