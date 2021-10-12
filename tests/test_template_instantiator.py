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
from gtwrap.interface_parser import (Argument, ArgumentList, Class,
                                     Constructor, Include, Method, Namespace,
                                     ReturnType, StaticMethod, Typename)


class TestInstantiationHelper(unittest.TestCase):
    """Tests for the InstantiationHelper class."""
    def test_constructor(self):
        pass

    def test_instantiate(self):
        pass

    def test_multilevel_instantiation(self):
        pass


class TestInstantiatedGlobalFunction(unittest.TestCase):
    """Tests for the InstantiatedGlobalFunction class."""
    def test_constructor(self):
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedConstructor(unittest.TestCase):
    """Tests for the InstantiatedConstructor class."""
    def test_constructor(self):
        pass

    def test_construct(self):
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedMethod(unittest.TestCase):
    """Tests for the InstantiatedMethod class."""
    def test_constructor(self):
        pass

    def test_construct(self):
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedStaticMethod(unittest.TestCase):
    """Tests for the InstantiatedStaticMethod class."""
    def test_constructor(self):
        pass

    def test_construct(self):
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedClass(unittest.TestCase):
    """Tests for the InstantiatedClass class."""
    def test_constructor(self):
        pass

    def test_instantiate_ctors(self):
        pass

    def test_instantiate_static_methods(self):
        pass

    def test_instantiate_methods(self):
        pass

    def test_instantiate_operators(self):
        pass

    def test_instantiate_properties(self):
        pass

    def test_cpp_typename(self):
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedDeclaration(unittest.TestCase):
    """Tests for the InstantiatedDeclaration class."""
    def test_constructor(self):
        pass

    def test_to_cpp(self):
        pass


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
        instantiations = [Typename.rule.parseString("double")[0]]
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
        instantiations = [Typename.rule.parseString("Man")[0]]
        instantiated_name = template_instantiator.instantiate_name(
            "Iron", instantiations)
        self.assertEqual(instantiated_name, "IronMan")

    def test_instantiate_namespace(self):
        """Test for instantiate_namespace."""
        namespace = Namespace.rule.parseString("""
            namespace gtsam {
                #include <gtsam/nonlinear/Values.h>
                template<T={gtsam::Basis}>
                class Values {
                    Values(const T& other);

                    template<V={Vector, Matrix}>
                    void insert(size_t j, V x);

                    template<S={double}>
                    static S staticMethod(const S& s);
                };
            }
        """)[0]
        instantiated_namespace = template_instantiator.instantiate_namespace(
            namespace)

        self.assertEqual(instantiated_namespace.name, "gtsam")
        self.assertEqual(instantiated_namespace.parent, "")

        self.assertEqual(instantiated_namespace.content[0].header,
                         "gtsam/nonlinear/Values.h")
        self.assertIsInstance(instantiated_namespace.content[0], Include)

        self.assertEqual(instantiated_namespace.content[1].name, "ValuesBasis")
        self.assertIsInstance(instantiated_namespace.content[1], Class)

        self.assertIsInstance(instantiated_namespace.content[1].ctors[0],
                              Constructor)
        self.assertEqual(instantiated_namespace.content[1].ctors[0].name,
                         "ValuesBasis")

        self.assertIsInstance(instantiated_namespace.content[1].methods[0],
                              Method)
        self.assertIsInstance(instantiated_namespace.content[1].methods[1],
                              Method)
        self.assertEqual(instantiated_namespace.content[1].methods[0].name,
                         "insertVector")
        self.assertEqual(instantiated_namespace.content[1].methods[1].name,
                         "insertMatrix")

        self.assertIsInstance(
            instantiated_namespace.content[1].static_methods[0], StaticMethod)
        self.assertEqual(
            instantiated_namespace.content[1].static_methods[0].name,
            "staticMethodDouble")


if __name__ == '__main__':
    unittest.main()
