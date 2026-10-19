// A separate static Boost runtime must not steal the managed registrations.
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/serialization/export.hpp>
#include "types.h"
#include <sstream>
BOOST_CLASS_EXPORT_GUID(example::First, "unrelated::First")
BOOST_CLASS_EXPORT_GUID(example::Second, "unrelated::Second")
#if defined(_WIN32)
#define TEST_EXPORT __declspec(dllexport)
#else
#define TEST_EXPORT __attribute__((visibility("default")))
#endif
extern "C" TEST_EXPORT int unrelated_roundtrip() {
  example::HolderA value(1);
  std::stringstream stream;
  { boost::archive::text_oarchive archive(stream); archive << value; }
  if (stream.str().find("unrelated::First") == std::string::npos) return 1;
  value.value.reset();
  { boost::archive::text_iarchive archive(stream); archive >> value; }
  return value.get() == 42 ? 0 : 2;
}
