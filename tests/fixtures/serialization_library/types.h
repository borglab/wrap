#pragma once
#include <boost/serialization/base_object.hpp>
#include <boost/serialization/shared_ptr.hpp>
#include <memory>

namespace example {
struct Base {
  virtual ~Base() = default;
  virtual int get() const { return 0; }
  template <class Archive> void serialize(Archive&, unsigned int) {}
};
struct First : Base {
  int value = 42;
  int get() const override { return value; }
  template <class Archive> void serialize(Archive& archive, unsigned int) {
    archive & boost::serialization::base_object<Base>(*this) & value;
  }
};
struct Second : Base {
  int value = 7;
  int get() const override { return value; }
  template <class Archive> void serialize(Archive& archive, unsigned int) {
    archive & boost::serialization::base_object<Base>(*this) & value;
  }
};
template<class A, class B> struct Pair : Base {
  A first = 3;
  B second = 1.5;
  int get() const override { return static_cast<int>(first); }
  template <class Archive> void serialize(Archive& archive, unsigned int) {
    archive & boost::serialization::base_object<Base>(*this) & first & second;
  }
};
template<int Tag> struct Holder {
  std::shared_ptr<Base> value;
  Holder() = default;
  explicit Holder(int kind) {
    if (kind == 1) value = std::make_shared<First>();
    else if (kind == 3) value = std::make_shared<Pair<int, double>>();
    else value = std::make_shared<Second>();
  }
  int get() const { return value ? value->get() : 0; }
  template <class Archive> void serialize(Archive& archive, unsigned int) {
    archive & value;
  }
};
using HolderA = Holder<1>;
using HolderB = Holder<2>;
}
