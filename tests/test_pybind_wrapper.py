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

from gtwrap.pybind_wrapper import PybindWrapper

sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))


class TestWrap(unittest.TestCase):
    """Tests for Python wrapper based on Pybind11."""
    TEST_DIR = osp.dirname(osp.realpath(__file__))
    INTERFACE_DIR = osp.join(TEST_DIR, 'fixtures')
    PYTHON_TEST_DIR = osp.join(TEST_DIR, 'expected', 'python')
    PYTHON_ACTUAL_DIR = osp.join(TEST_DIR, "actual", "python")

    # Create the `actual/python` directory
    os.makedirs(PYTHON_ACTUAL_DIR, exist_ok=True)

    def wrap_content(self,
                     sources,
                     module_name,
                     output_dir,
                     use_boost_serialization=False,
                     module_template=None):
        """
        Common function to wrap content in `sources`.
        """
        if module_template is None:
            with open(osp.join(self.TEST_DIR, "pybind_wrapper.tpl"),
                      encoding="UTF-8") as template_file:
                module_template = template_file.read()

        # Create Pybind wrapper instance
        wrapper = PybindWrapper(
            module_name=module_name,
            top_module_namespaces=[''],
            ignore_classes=[''],
            module_template=module_template,
            use_boost_serialization=use_boost_serialization)

        output = osp.join(self.TEST_DIR, output_dir, module_name + ".cpp")

        if not osp.exists(osp.join(self.TEST_DIR, output_dir)):
            os.mkdir(osp.join(self.TEST_DIR, output_dir))

        wrapper.wrap(sources, output)

        return output

    def compare_and_diff(self, file, actual):
        """
        Compute the comparison between the expected and actual file,
        and assert if diff is zero.
        """
        expected = osp.join(self.PYTHON_TEST_DIR, file)
        success = filecmp.cmp(actual, expected, shallow=False)

        if not success:
            os.system(f"diff {actual} {expected}")
        self.assertTrue(success, f"Mismatch for file {file}")

    def test_geometry(self):
        """
        Check generation of python geometry wrapper.
        python3 ../pybind_wrapper.py --src geometry.h --module_name
            geometry_py --out output/geometry_py.cc
        """
        source = osp.join(self.INTERFACE_DIR, 'geometry.i')
        output = self.wrap_content([source],
                                   'geometry_py',
                                   self.PYTHON_ACTUAL_DIR,
                                   use_boost_serialization=True)

        self.compare_and_diff('geometry_pybind.cpp', output)

    def test_functions(self):
        """Test interface file with function info."""
        source = osp.join(self.INTERFACE_DIR, 'functions.i')
        output = self.wrap_content([source], 'functions_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('functions_pybind.cpp', output)

    def test_class(self):
        """Test interface file with only class info."""
        source = osp.join(self.INTERFACE_DIR, 'class.i')
        output = self.wrap_content([source], 'class_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('class_pybind.cpp', output)

    def test_templates(self):
        """Test interface file with templated class."""
        source = osp.join(self.INTERFACE_DIR, 'templates.i')
        output = self.wrap_content([source], 'templates_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('templates_pybind.cpp', output)

    def test_inheritance(self):
        """Test interface file with class inheritance definitions."""
        source = osp.join(self.INTERFACE_DIR, 'inheritance.i')
        output = self.wrap_content([source], 'inheritance_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('inheritance_pybind.cpp', output)

    def test_namespaces(self):
        """
        Check generation of python wrapper for full namespace definition.
        python3 ../pybind_wrapper.py --src namespaces.i --module_name
            namespaces_py --out output/namespaces_py.cpp
        """
        source = osp.join(self.INTERFACE_DIR, 'namespaces.i')
        output = self.wrap_content([source], 'namespaces_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('namespaces_pybind.cpp', output)

    def test_operator_overload(self):
        """
        Tests for operator overloading.
        """
        source = osp.join(self.INTERFACE_DIR, 'operator.i')
        output = self.wrap_content([source], 'operator_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('operator_pybind.cpp', output)

    def test_special_cases(self):
        """
        Tests for some unique, non-trivial features.
        """
        source = osp.join(self.INTERFACE_DIR, 'special_cases.i')
        output = self.wrap_content([source], 'special_cases_py',
                                   self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('special_cases_pybind.cpp', output)

    def test_enum(self):
        """
        Test if enum generation is correct.
        """
        source = osp.join(self.INTERFACE_DIR, 'enum.i')
        output = self.wrap_content([source], 'enum_py', self.PYTHON_ACTUAL_DIR)

        self.compare_and_diff('enum_pybind.cpp', output)

    def test_argument_policy_hook(self):
        """Test that typed args are emitted through the overridable policy hook."""
        source = osp.join(self.INTERFACE_DIR, 'arg_policies.i')
        module_template = """#include <pybind11/pybind11.h>

{includes}

#include "python/arg_policy_preamble.h"

namespace py = pybind11;

PYBIND11_MODULE({module_name}, m_) {{
    m_.doc() = "pybind11 wrapper of {module_name}";

{wrapped_namespace}

}}
"""
        output = self.wrap_content([source],
                                   'arg_policies_py',
                                   self.PYTHON_ACTUAL_DIR,
                                   module_template=module_template)

        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()

        self.assertLess(content.index('template <typename T>\nstruct PyArgPolicy'),
                        content.index('#include "python/arg_policy_preamble.h"'))
        self.assertIn(
            'gtwrap::internal::py_arg<const testing::SpecialView&>("values")',
            content)
        self.assertIn('gtwrap::internal::py_arg<int>("count") = 1', content)
        self.assertIn('.def("noConvert",&testing::ArgPolicyFixture::noConvert',
                      content)

    def test_direct_callable_bindings(self):
        """Test direct pointers and overload casts for ordinary callables."""
        source = osp.join(self.INTERFACE_DIR, 'class.i')
        output = self.wrap_content([source], 'class_py',
                                   self.PYTHON_ACTUAL_DIR)

        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()

        # Unambiguous const/non-const methods and static methods use pointers.
        self.assertIn('.def("return_bool",&Test::return_bool', content)
        self.assertIn('.def("push_back",&Test::push_back', content)
        self.assertIn('.def_static("create",&FunRange::create)', content)

        # Python-only renaming does not require an adapter.
        self.assertIn('.def("lambda_",&Test::lambda)', content)
        self.assertIn('.def("_repr_markdown_",&Test::markdown', content)

        # Ordinary const overloads use py::overload_cast with py::const_.
        self.assertIn(
            'py::overload_cast<const gtsam::Vector&, const gtsam::Matrix&>'
            '(&Test::return_pair, py::const_)', content)

        source = osp.join(self.INTERFACE_DIR, 'geometry.i')
        output = self.wrap_content([source],
                                   'geometry_py',
                                   self.PYTHON_ACTUAL_DIR,
                                   use_boost_serialization=True)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()
        self.assertIn(
            '.def_static("staticFunction",&gtsam::Point3::staticFunction)',
            content)

        source = osp.join(self.INTERFACE_DIR, 'functions.i')
        output = self.wrap_content([source], 'functions_py',
                                   self.PYTHON_ACTUAL_DIR)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()
        self.assertIn('m_.def("aGlobalFunction",&::aGlobalFunction)', content)
        self.assertIn(
            'py::overload_cast<int, double>(&::overloadedGlobalFunction)',
            content)

    def test_mutable_output_and_static_overloads(self):
        """Test pointer bindings for mutable output args and static overloads."""
        source = osp.join(self.INTERFACE_DIR, 'eigen_ref.i')
        output = self.wrap_content([source], 'eigen_ref_py',
                                   self.PYTHON_ACTUAL_DIR)

        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()

        self.assertIn(
            'py::overload_cast<const gtsam::Point3&, '
            'Eigen::Ref<Eigen::MatrixXd>, Eigen::Ref<Eigen::MatrixXd>>'
            '(&gtsam::Pose3::transformFrom, py::const_)', content)
        self.assertIn(
            'py::overload_cast<gtsam::Vector, Eigen::Ref<Eigen::MatrixXd>>'
            '(&gtsam::Pose3::Expmap)', content)
        self.assertNotIn('[](', content)

    def test_member_static_name_collision(self):
        """Test overload detection across member and static method lists."""
        with open(osp.join(self.TEST_DIR, "pybind_wrapper.tpl"),
                  encoding="UTF-8") as template_file:
            module_template = template_file.read()

        wrapper = PybindWrapper(module_name='mixed_py',
                                top_module_namespaces=[''],
                                module_template=module_template)
        content = wrapper.wrap_file(
            'class Mixed { int call(int value); '
            'static int call(double value); };',
            module_name='mixed_py')

        self.assertIn('py::overload_cast<int>(&Mixed::call)', content)
        self.assertIn('py::overload_cast<double>(&Mixed::call)', content)
        self.assertNotIn('[](', content)

    def test_lambda_adapters_are_preserved(self):
        """Test that non-forwarding and specialized bindings retain lambdas."""
        source = osp.join(self.INTERFACE_DIR, 'class.i')
        output = self.wrap_content([source], 'class_py',
                                   self.PYTHON_ACTUAL_DIR)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()

        self.assertIn(
            '.def("templatedMethodString",[](Fun<double>* self', content)
        self.assertIn('.def("print",[](Test* self)', content)
        self.assertIn('.def("__repr__",\n                    [](', content)
        self.assertIn('.def("__len__",[](FastSet* self)', content)

        source = osp.join(self.INTERFACE_DIR, 'geometry.i')
        output = self.wrap_content([source],
                                   'geometry_py',
                                   self.PYTHON_ACTUAL_DIR,
                                   use_boost_serialization=True)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()
        self.assertIn('.def("serialize", [](gtsam::Point2* self)', content)
        self.assertIn('.def(py::pickle(', content)

        source = osp.join(self.INTERFACE_DIR, 'namespaces.i')
        output = self.wrap_content([source], 'namespaces_py',
                                   self.PYTHON_ACTUAL_DIR)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()
        self.assertIn('.def("insert_vector",[](gtsam::Values* self', content)

        source = osp.join(self.INTERFACE_DIR, 'functions.i')
        output = self.wrap_content([source], 'functions_py',
                                   self.PYTHON_ACTUAL_DIR)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()
        self.assertIn(
            'm_.def("MultiTemplatedFunctionStringSize_tDouble",[](', content)

        source = osp.join(self.INTERFACE_DIR, 'special_cases.i')
        output = self.wrap_content([source], 'special_cases_py',
                                   self.PYTHON_ACTUAL_DIR)
        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()
        self.assertIn(
            '.def("addPriorPinholeCameraCal3Bundler",[](', content)

    def test_direct_pointer_preserves_docstring(self):
        """Test that direct member pointers retain generated docstrings."""
        with open(osp.join(self.TEST_DIR, "pybind_wrapper.tpl"),
                  encoding="UTF-8") as template_file:
            module_template = template_file.read()

        wrapper = PybindWrapper(module_name='docstring_py',
                                top_module_namespaces=[''],
                                module_template=module_template,
                                xml_source='unused')
        wrapper.xml_parser.extract_docstring = lambda *args: 'A docstring.'
        content = wrapper.wrap_file('class DocClass { int value() const; };',
                                    module_name='docstring_py')

        self.assertIn(
            '.def("value",&DocClass::value, "A docstring.")', content)

    def test_const_ref_return_policy(self):
        """Test that methods returning const T& emit reference_internal policy.

        Without this policy, pybind11 defaults to copying the returned reference.
        With the policy, the binding keeps the reference alive via the parent object.

        Direct pointers preserve the C++ reference return type, while
        reference_internal keeps the returned reference tied to its parent.
        """
        source = osp.join(self.INTERFACE_DIR, 'class.i')
        output = self.wrap_content([source], 'class_py',
                                   self.PYTHON_ACTUAL_DIR)

        with open(output, 'r') as f:
            content = f.read()

        self.assertIn(
            'static_cast<const gtsam::Vector& (Test::*)'
            '(const gtsam::Vector&) const>(&Test::return_vector2), '
            'py::return_value_policy::reference_internal', content)
        self.assertIn(
            'static_cast<const gtsam::Matrix& (Test::*)'
            '(const gtsam::Matrix&) const>(&Test::return_matrix2), '
            'py::return_value_policy::reference_internal', content)

        # Non-ref returns (e.g. return_vector1 which returns by value) should NOT
        lines = content.split('\n')
        for line in lines:
            if 'return_vector1' in line:
                self.assertNotIn('reference_internal', line)
                self.assertIn('&Test::return_vector1', line)
            if 'return_matrix1' in line:
                self.assertNotIn('reference_internal', line)
                self.assertIn('&Test::return_matrix1', line)

        source = osp.join(self.INTERFACE_DIR, 'return_policies.i')
        output = self.wrap_content([source], 'return_policies_py',
                                   self.PYTHON_ACTUAL_DIR)

        with open(output, 'r', encoding='UTF-8') as f:
            content = f.read()

        for line in content.split('\n'):
            if 'return_const_ref' in line:
                self.assertIn('reference_internal', line)
                self.assertIn('&ReturnPolicyFixture::return_const_ref', line)
                self.assertNotIn('[](', line)
            if '.def("return_mutable_ref"' in line or '.def("return_value"' in line:
                self.assertNotIn('reference_internal', line)
                self.assertIn('&ReturnPolicyFixture::', line)
                self.assertNotIn('[](', line)


if __name__ == '__main__':
    unittest.main()
