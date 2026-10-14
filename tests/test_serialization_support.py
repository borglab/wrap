"""Shared Boost export generation and cross-translation-unit registration."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from gtwrap.pybind_wrapper import PybindWrapper


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests' / 'fixtures'


class TestSerializationSupport(unittest.TestCase):

    def test_selected_keys_and_implementations(self):
        source = (FIXTURES / 'serialization_shared.i').read_text()
        wrapper = PybindWrapper('', top_module_namespaces=[''],
                                use_boost_serialization=True)
        keys, implementations = wrapper.serialization_support(
            source, 'example::', ['serialization_shared.h'])
        self.assertIn('#include <serialization_shared.h>', keys)
        self.assertEqual(keys.count('BOOST_CLASS_EXPORT_KEY('), 2)
        self.assertEqual(implementations.count('BOOST_CLASS_EXPORT_IMPLEMENT('), 2)
        self.assertIn('BOOST_CLASS_EXPORT_KEY(example::First)', keys)
        self.assertIn('BOOST_CLASS_EXPORT_KEY(example::Second)', keys)
        self.assertNotIn('unrelated::Third', keys + implementations)
        self.assertEqual(wrapper._serializing_classes, [])

    def test_comma_containing_type_keeps_existing_archive_name(self):
        source = '''namespace example {
template<A, B> class Pair {};
@serializable
typedef example::Pair<int, double> PairID;
}'''
        wrapper = PybindWrapper('', top_module_namespaces=[''],
                                use_boost_serialization=True)
        keys, implementations = wrapper.serialization_support(
            source, 'example::')
        self.assertIn('typedef example::Pair<int, double> examplePairintdouble;',
                      keys)
        self.assertIn('BOOST_CLASS_EXPORT_KEY(examplePairintdouble)', keys)
        self.assertEqual(implementations,
                         'BOOST_CLASS_EXPORT_IMPLEMENT(examplePairintdouble)\n')

    def test_cli_and_cross_translation_unit_round_trip(self):
        compiler = shutil.which('c++')
        boost_lib = next((path for path in
                          ('/opt/homebrew/lib', '/usr/local/lib',
                           '/usr/lib/x86_64-linux-gnu', '/usr/lib')
                          if list(Path(path).glob('libboost_serialization.*'))),
                         None)
        if not compiler or not boost_lib:
            self.skipTest('C++ compiler or Boost.Serialization library unavailable')

        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            subprocess.run([
                sys.executable, str(ROOT / 'scripts' / 'pybind_serialization.py'),
                '--src', str(FIXTURES / 'serialization_shared.i'),
                '--namespace-prefix', 'example::',
                '--include', 'serialization_shared.h',
                '--out-header', str(directory / 'keys.h'),
                '--out-implementations', str(directory / 'implementations.inc'),
            ], check=True, env={**os.environ, 'PYTHONPATH': str(ROOT)})

            # The first owner mirrors stable's existing full exports. The
            # second mirrors unstable's keys plus implementation fragment.
            # Each is compiled separately with a consumer translation unit.
            consumers = r'''
#include "keys.h"
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/serialization/shared_ptr.hpp>
#include <memory>
#include <sstream>
int main() {
  if (std::string(boost::serialization::guid<example::First>()) !=
      "example::First") return 1;
  std::shared_ptr<example::Base> value = std::make_shared<example::First>();
  std::stringstream stream;
  { boost::archive::text_oarchive archive(stream); archive << value; }
  value.reset();
  { boost::archive::text_iarchive archive(stream); archive >> value; }
  auto result = std::dynamic_pointer_cast<example::First>(value);
  return result && result->value == 42 ? 0 : 2;
}
'''
            (directory / 'consumer.cpp').write_text(consumers)
            archive_headers = '''#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
'''
            owners = {
                'full': archive_headers + '''#include "serialization_shared.h"
#include <boost/serialization/export.hpp>
BOOST_CLASS_EXPORT(example::First)
BOOST_CLASS_EXPORT(example::Second)
''',
                'split': archive_headers + '''#include "keys.h"
#include "implementations.inc"
''',
            }
            libraries = {}
            for name, owner in owners.items():
                with self.subTest(owner=name):
                    (directory / 'owner.cpp').write_text(owner)
                    executable = directory / name
                    build = subprocess.run([
                        compiler, '-std=c++17', '-I', str(directory),
                        '-I', str(Path(boost_lib).parent / 'include'),
                        '-I', str(FIXTURES), str(directory / 'owner.cpp'),
                        str(directory / 'consumer.cpp'), '-L', boost_lib,
                        '-lboost_serialization', '-o', str(executable),
                    ], capture_output=True, text=True)
                    self.assertEqual(build.returncode, 0, build.stderr)
                    subprocess.run([str(executable)], check=True,
                                   env={**os.environ,
                                        'DYLD_LIBRARY_PATH': boost_lib,
                                        'LD_LIBRARY_PATH': boost_lib})

                    # Two extensions each own their implementations. Loading
                    # either first must not change the archive identifier or
                    # prevent the other from round-tripping the derived type.
                    (directory / 'consumer.cpp').write_text(
                        consumers.replace('int main()',
                                          'extern "C" int roundtrip()'))
                    library = directory / f'lib{name}{".dylib" if sys.platform == "darwin" else ".so"}'
                    shared = subprocess.run([
                        compiler, '-std=c++17', '-shared', '-fPIC',
                        '-I', str(directory),
                        '-I', str(Path(boost_lib).parent / 'include'),
                        '-I', str(FIXTURES), str(directory / 'owner.cpp'),
                        str(directory / 'consumer.cpp'), '-L', boost_lib,
                        f'-Wl,-rpath,{boost_lib}', '-lboost_serialization',
                        '-o', str(library),
                    ], capture_output=True, text=True)
                    self.assertEqual(shared.returncode, 0, shared.stderr)
                    libraries[name] = library
                    (directory / 'consumer.cpp').write_text(consumers)

            load_script = '''import ctypes, sys
for path in sys.argv[1:]:
    library = ctypes.CDLL(path)
    assert library.roundtrip() == 0
'''
            for order in (('full',), ('full', 'split'), ('split', 'full')):
                with self.subTest(import_order=order):
                    run = subprocess.run([
                        sys.executable, '-c', load_script,
                        *(str(libraries[name]) for name in order),
                    ], capture_output=True, text=True,
                        env={**os.environ, 'DYLD_LIBRARY_PATH': boost_lib,
                             'LD_LIBRARY_PATH': boost_lib})
                    self.assertEqual(run.returncode, 0,
                                     run.stdout + run.stderr)


if __name__ == '__main__':
    unittest.main()
