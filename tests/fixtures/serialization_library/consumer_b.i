namespace example {
#include <types.h>
class HolderB {
  HolderB();
  HolderB(int kind);
  int get() const;
  void serializable() const;
};
}
