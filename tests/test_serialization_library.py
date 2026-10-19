"""The generated ABI keeps archive implementation details in one owner."""
import json
import unittest

from gtwrap.serialization_library import generate_library


class TestLibraryGeneration(unittest.TestCase):
    def test_private_exports_and_stable_abi(self):
        source = '''namespace example {
template<A, B> class Pair {};
@serializable typedef example::Pair<int, double> PairID;
}'''
        files = generate_library('registry', [('types.i', source)], ['types.h'])
        manifest = json.loads(files['registry.json'])
        entry, = manifest['entries']
        self.assertEqual(entry['export_name'], 'examplePairintdouble')
        self.assertNotIn('BOOST_CLASS_EXPORT', files['registry.h'])
        self.assertNotIn('boost/archive', files['registry.h'])
        self.assertIn('BOOST_CLASS_EXPORT_KEY(examplePairintdouble)', files['registry_keys.h'])
        self.assertIn('BOOST_CLASS_EXPORT_IMPLEMENT(examplePairintdouble)', files['registry.cpp'])
        self.assertIn('throw std::runtime_error(error.what())', files['registry.cpp'])
        self.assertIn(entry['save'] + ';', files['registry.map'])
        self.assertIn('_' + entry['load'] + '\n', files['registry.exports'])
        self.assertEqual(files, generate_library('registry', [('types.i', source)], ['types.h']))
