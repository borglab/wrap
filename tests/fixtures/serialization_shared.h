#pragma once

#include <boost/serialization/base_object.hpp>

namespace example {
struct Base {
  virtual ~Base() = default;
  template <class Archive>
  void serialize(Archive&, unsigned int) {}
};

struct First : Base {
  int value = 42;
  template <class Archive>
  void serialize(Archive& archive, unsigned int) {
    archive & boost::serialization::base_object<Base>(*this);
    archive & value;
  }
};

struct Second : Base {
  int value = 7;
  template <class Archive>
  void serialize(Archive& archive, unsigned int) {
    archive & boost::serialization::base_object<Base>(*this);
    archive & value;
  }
};
}
