namespace example {
#include <types.h>
class HolderA {
  HolderA();
  HolderA(int kind);
  int get() const;
  void serializable() const;
};
}
