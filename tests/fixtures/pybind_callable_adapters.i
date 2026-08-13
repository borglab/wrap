#include <pybind_callable_adapters.h>

namespace adapters {

class BaseAdapter {
  BaseAdapter();

  int inherited(int value) const;
};

template<T = {int}>
class Adapter: adapters::BaseAdapter {
  Adapter();

  int exact(int value);
  int exactConst(int value) const;
  static int exactStatic(int value);

  int omittedDefault(int value) const;

  int referenceArgument(int value) const;

  int hiddenOverload(int value) const;

  int declaredOverload(int value) const;
  double declaredOverload(double value) const;

  T at(size_t index) const;

  T front() const;

  int alias(int index) const;

  static int staticOmitted(int value);

  template<U = {double}>
  U exactTemplated(U value) const;

  template<U = {double}>
  U adaptedTemplated(U value) const;

  const string& lambda(const string& value = "fallback") const;
};

int exactGlobal(int value);

int globalOmitted(int value);

int globalHidden(int value);

int globalOverload(int value);
double globalOverload(double value);

template<T = {int}>
T exactGlobalTemplated(T value);

template<T = {int}>
T adaptedGlobalTemplated(T value);

}
