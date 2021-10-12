"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Tests for template_instantiator.

Author: Varun Agrawal
"""

# pylint: disable=import-error,wrong-import-position

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gtwrap import template_instantiator
from gtwrap.interface_parser import (Argument, ArgumentList, ReturnType,
                                     Typename)


class TestTemplateInstantiator(unittest.TestCase):
    """
    Test overall template instantiation and the functions in the module.
    """
    def test_scoped_template(self):
        """Test is_scoped_template."""
        # Test if not scoped template.
        template_typenames = ['T']
        str_arg_typename = "double"
        scoped_template, scoped_idx = template_instantiator.is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertFalse(scoped_template)
        self.assertEqual(scoped_idx, -1)

        # Check for correct template match.
        template_typenames = ['T']
        str_arg_typename = "gtsam::Matrix"
        scoped_template, scoped_idx = template_instantiator.is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertFalse(scoped_template)
        self.assertEqual(scoped_idx, -1)

        # Test scoped templatte
        template_typenames = ['T']
        str_arg_typename = "T::Value"
        scoped_template, scoped_idx = template_instantiator.is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertEqual(scoped_template, "T")
        self.assertEqual(scoped_idx, 0)

        template_typenames = ['U', 'T']
        str_arg_typename = "T::Value"
        scoped_template, scoped_idx = template_instantiator.is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertEqual(scoped_template, "T")
        self.assertEqual(scoped_idx, 1)

    def test_instantiate_type(self):
        """Test for instantiate_type."""
        arg = Argument.rule.parseString("const T x")[0]
        template_typenames = ["T"]
        instantiations = [Typename.rule.parseString("double")[0]]
        cpp_typename = "ExampleClass"
        new_type = template_instantiator.instantiate_type(
            arg.ctype,
            template_typenames,
            instantiations=instantiations,
            cpp_typename=cpp_typename,
            instantiated_class=None)

        new_typename = new_type.typename
        self.assertEqual(new_typename.name, "double")
        self.assertEqual(new_typename.instantiated_name(), "double")

    def test_instantiate_args_list(self):
        """Test for instantiate_args_list."""
        args = ArgumentList.rule.parseString("T x, double y, string z")[0]
        args_list = args.list()
        template_typenames = ['T']
        instantiations = [Typename.rule.parseString("double")[0]]
        instantiated_args_list = template_instantiator.instantiate_args_list(
            args_list,
            template_typenames,
            instantiations,
            cpp_typename="ExampleClass")

        self.assertEqual(instantiated_args_list[0].ctype.get_typename(),
                         "double")

        args = ArgumentList.rule.parseString("T x, U y, string z")[0]
        args_list = args.list()
        template_typenames = ['T', 'U']
        instantiations = [
            Typename.rule.parseString("double")[0],
            Typename.rule.parseString("Matrix")[0]
        ]
        instantiated_args_list = template_instantiator.instantiate_args_list(
            args_list,
            template_typenames,
            instantiations,
            cpp_typename="ExampleClass")
        self.assertEqual(instantiated_args_list[0].ctype.get_typename(),
                         "double")
        self.assertEqual(instantiated_args_list[1].ctype.get_typename(),
                         "Matrix")

        args = ArgumentList.rule.parseString("T x, U y, T z")[0]
        args_list = args.list()
        template_typenames = ['T', 'U']
        instantiations = [
            Typename.rule.parseString("double")[0],
            Typename.rule.parseString("Matrix")[0]
        ]
        instantiated_args_list = template_instantiator.instantiate_args_list(
            args_list,
            template_typenames,
            instantiations,
            cpp_typename="ExampleClass")
        self.assertEqual(instantiated_args_list[0].ctype.get_typename(),
                         "double")
        self.assertEqual(instantiated_args_list[1].ctype.get_typename(),
                         "Matrix")
        self.assertEqual(instantiated_args_list[2].ctype.get_typename(),
                         "double")

    def test_instantiate_return_type(self):
        """Test for instantiate_return_type."""
        return_type = ReturnType.rule.parseString("T")[0]
        template_typenames = ['T']
        instantiations = [
            Typename.rule.parseString("double")[0],
        ]
        instantiated_return_type = template_instantiator.instantiate_return_type(
            return_type,
            template_typenames,
            instantiations,
            cpp_typename="ExampleClass")

        self.assertEqual(instantiated_return_type.type1.get_typename(),
                         "double")

        return_type = ReturnType.rule.parseString("pair<T, U>")[0]
        template_typenames = ['T', 'U']
        instantiations = [
            Typename.rule.parseString("double")[0],
            Typename.rule.parseString("char")[0],
        ]
        instantiated_return_type = template_instantiator.instantiate_return_type(
            return_type,
            template_typenames,
            instantiations,
            cpp_typename="ExampleClass")

        self.assertEqual(instantiated_return_type.type1.get_typename(),
                         "double")
        self.assertEqual(instantiated_return_type.type2.get_typename(), "char")

    def test_instantiate_name(self):
        """Test for instantiate_name."""
        pass

    def test_instantiate_namespace(self):
        """Test for instantiate_namespace."""
        pass


if __name__ == '__main__':
    unittest.main()
