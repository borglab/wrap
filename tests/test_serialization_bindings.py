"""Managed methods call the archive owner; legacy generation remains opt-in."""
import json
from pathlib import Path
import tempfile
import unittest

from gtwrap.pybind_wrapper import PybindWrapper
from gtwrap.serialization_library import generate_library, write_library


class TestManagedBindings(unittest.TestCase):
    def test_managed_and_unselected_types(self):
        source = '''namespace example {
class Managed { Managed(); void serializable() const; };
class Local { Local(); void serialize() const; };
}'''
        template = Path(__file__).with_name('pybind_wrapper.tpl').read_text()
        with tempfile.TemporaryDirectory() as directory:
            files = generate_library('registry', [('types.i', source)], ['types.h'],
                                     ignore_classes=['example::Local'])
            write_library(directory, files)
            manifest = Path(directory) / 'registry.json'
            wrapper = PybindWrapper('example', top_module_namespaces=[''],
                                    use_boost_serialization=True,
                                    module_template=template,
                                    serialization_manifest=manifest)
            output = wrapper.wrap_file(source, module_name='example', submodules=[])
            entry = json.loads(files['registry.json'])['entries'][0]
            self.assertIn(entry['save'] + '(self, &result)', output)
            self.assertIn(entry['load'] + '(&input, &value)', output)
            self.assertIn('BOOST_CLASS_EXPORT(example::Local)', output)
            self.assertNotIn('BOOST_CLASS_EXPORT(example::Managed)', output)
            self.assertIn('#include "registry.h"', output)
            with self.assertRaisesRegex(ValueError, 'requires serialization enabled'):
                PybindWrapper('example', serialization_manifest=manifest)

    def test_disabled_has_no_runtime_dependency(self):
        source = 'class Plain { Plain(); void serialize() const; };'
        template = Path(__file__).with_name('pybind_wrapper.tpl').read_text()
        output = PybindWrapper('plain', top_module_namespaces=[''],
                               module_template=template).wrap_file(
                                   source, module_name='plain', submodules=[])
        self.assertNotIn('.def("serialize"', output)
        self.assertNotIn('boost/serialization', output)
