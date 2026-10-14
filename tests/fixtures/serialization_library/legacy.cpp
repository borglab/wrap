#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/serialization/export.hpp>
#include "types.h"
#include <fstream>
#include <string>

BOOST_CLASS_EXPORT(example::First)
BOOST_CLASS_EXPORT(example::Second)
typedef example::Pair<int, double> examplePairintdouble;
BOOST_CLASS_EXPORT(examplePairintdouble)
BOOST_CLASS_EXPORT(example::HolderA)

int main(int argc, char** argv) {
  if (argc != 3) return 1;
  example::HolderA value(1);
  if (std::string(argv[1]) == "save") {
    std::ofstream stream(argv[2]);
    boost::archive::text_oarchive archive(stream);
    archive << value;
  } else {
    std::ifstream stream(argv[2]);
    boost::archive::text_iarchive archive(stream);
    archive >> value;
    if (value.get() != 42) return 2;
  }
}
