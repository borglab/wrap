"""
Unit test for Pybind wrap program
Author: Matthew Sklar, Varun Agrawal
Date: February 2019
"""

# pylint: disable=import-error, wrong-import-position, too-many-branches

import filecmp
import os
import os.path as osp
import sys
import unittest

sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))
sys.path.append(
    osp.normpath(osp.abspath(osp.join(__file__, '../../../build/wrap'))))

import gtwrap.interface_parser as parser
import gtwrap.template_instantiator as instantiator
from gtwrap.pybind_wrapper import PybindWrapper

sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))


class TestWrap(unittest.TestCase):
    """Tests for Python wrapper based on Pybind11."""
    TEST_DIR = osp.dirname(osp.realpath(__file__))

    def wrap_content(self, content, module_name, output_dir):
        """
        Common function to wrap content.
        """
        module = parser.Module.parseString(content)

        instantiator.instantiate_namespace_inplace(module)

        with open(osp.join(self.TEST_DIR,
                           "pybind_wrapper.tpl")) as template_file:
            module_template = template_file.read()

        # Create Pybind wrapper instance
        wrapper = PybindWrapper(module=module,
                                module_name=module_name,
                                use_boost=False,
                                top_module_namespaces=[''],
                                ignore_classes=[''],
                                module_template=module_template)

        cc_content = wrapper.wrap()

        output = osp.join(self.TEST_DIR, output_dir, module_name + ".cpp")

        if not osp.exists(osp.join(self.TEST_DIR, output_dir)):
            os.mkdir(osp.join(self.TEST_DIR, output_dir))

        with open(output, 'w') as f:
            f.write(cc_content)

        return output

    def test_geometry(self):
        """
        Check generation of python geometry wrapper.
        python3 ../pybind_wrapper.py --src geometry.h --module_name
            geometry_py --out output/geometry_py.cc
        """
        with open(osp.join(self.TEST_DIR, 'fixtures', 'geometry.h'), 'r') as f:
            content = f.read()

        output = self.wrap_content(content, 'geometry_py',
                                   osp.join('actual', 'python'))

        expected = osp.join(self.TEST_DIR, 'expected', 'python',
                            'geometry_pybind.cpp')
        success = filecmp.cmp(output, expected)

        if not success:
            os.system("diff {} {}".format(output, expected))
        self.assertTrue(success)

    def test_namespaces(self):
        """
        Check generation of python geometry wrapper.
        python3 ../pybind_wrapper.py --src testNamespaces.h --module_name
            testNamespaces_py --out output/testNamespaces_py.cc
        """
        with open(osp.join(self.TEST_DIR, 'testNamespaces.h'), 'r') as f:
            content = f.read()

        output = self.wrap_content(content, 'testNamespaces_py',
                                   osp.join('actual', 'python'))

        expected = osp.join(
            self.TEST_DIR,
            osp.join('expected', 'python', 'testNamespaces_py.cpp'))
        success = filecmp.cmp(output, expected)

        if not success:
            os.system("diff {} {}".format(output, expected))
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
