namespace example {
#include <serialization_shared.h>
virtual class Base {};
virtual class First : example::Base {
  void serializable() const;
};
virtual class Second : example::Base {
  void serializable() const;
};
}

namespace unrelated {
class Third {
  void serializable() const;
};
}
