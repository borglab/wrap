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

from gtwrap.interface_parser import (Argument, ArgumentList, Class,
                                     Constructor, ForwardDeclaration, Include,
                                     Method, Namespace, ReturnType,
                                     StaticMethod, Typename)
from gtwrap.template_instantiator import (
    InstantiatedClass, InstantiatedConstructor, InstantiatedDeclaration,
    InstantiatedMethod, InstantiationHelper, instantiate_args_list,
    instantiate_name, instantiate_namespace, instantiate_return_type,
    instantiate_type, is_scoped_template)


class TestInstantiationHelper(unittest.TestCase):
    """Tests for the InstantiationHelper class."""
    def test_constructor(self):
        """Test constructor."""
        helper = InstantiationHelper(InstantiatedClass)
        self.assertEqual(helper.instantiation_type, InstantiatedClass)

    def test_instantiate(self):
        """Test instantiate method."""
        pass

    def test_multilevel_instantiation(self):
        """
        Test method for multilevel instantiation
        i.e. instantiation at both the class and method level.
        """
        pass


class TestInstantiatedGlobalFunction(unittest.TestCase):
    """Tests for the InstantiatedGlobalFunction class."""
    def test_constructor(self):
        """Test constructor."""
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedConstructor(unittest.TestCase):
    """Tests for the InstantiatedConstructor class."""
    def setUp(self):
        constructor = Constructor.rule.parseString("""
            template<U={double}>
            Class(C x, const U& param);
            """)[0]
        instantiations = [
            Typename.rule.parseString("double")[0],
            Typename.rule.parseString("string")[0]
        ]
        self.constructor = InstantiatedConstructor(constructor, instantiations)

    def test_constructor(self):
        """Test constructor."""
        self.assertIsInstance(self.constructor, InstantiatedConstructor)
        self.assertIsInstance(self.constructor.original, Constructor)

    def test_construct(self):
        """Test the construct classmethod."""
        constructor = Constructor.rule.parseString("""
            template<U={double}>
            Class(C x, const U& param);
            """)[0]
        c = Class.rule.parseString("""
            template<C={string}>
            class Class {};
        """)[0]
        class_instantiations = [Typename.rule.parseString("double")[0]]
        method_instantiations = [Typename.rule.parseString("string")[0]]
        typenames = ['C', 'U']
        parent = InstantiatedClass(c, class_instantiations)
        instantiated_args = instantiate_args_list(
            constructor.args.list(),
            typenames, class_instantiations + method_instantiations,
            parent.cpp_typename())

        instantiated_constructor = InstantiatedConstructor.construct(
            constructor, typenames, class_instantiations,
            method_instantiations, instantiated_args, parent)
        self.assertEqual(instantiated_constructor.name, "ClassDouble")
        self.assertEqual(
            instantiated_constructor.args.list()[0].ctype.get_typename(),
            "double")
        self.assertEqual(
            instantiated_constructor.args.list()[1].ctype.get_typename(),
            "string")

    def test_to_cpp(self):
        """Test the to_cpp method."""
        actual = self.constructor.to_cpp()
        self.assertEqual(actual, "Class<double,string>")


class TestInstantiatedMethod(unittest.TestCase):
    """Tests for the InstantiatedMethod class."""
    def setUp(self):
        method = Method.rule.parseString("""
            template<U={double}>
            double method(const U& param);
            """)[0]
        instantiations = [Typename.rule.parseString("double")[0]]
        self.method = InstantiatedMethod(method, instantiations)

    def test_constructor(self):
        """Test constructor."""
        self.assertIsInstance(self.method, InstantiatedMethod)
        self.assertIsInstance(self.method.original, Method)
        self.assertEqual(self.method.name, "methodDouble")

    def test_construct(self):
        """Test the construct classmethod."""
        method = Method.rule.parseString("""
            template<U={double}>
            T method(U& param);
            """)[0]
        method_instantiations = [Typename.rule.parseString("double")[0]]
        c = Class.rule.parseString("""
            template<T={string}>
            class Class {};
        """)[0]
        class_instantiations = [Typename.rule.parseString("string")[0]]

        typenames = ['T', 'U']
        parent = InstantiatedClass(c, class_instantiations)
        instantiated_args = instantiate_args_list(
            method.args.list(),
            typenames, class_instantiations + method_instantiations,
            parent.cpp_typename())

        instantiated_method = InstantiatedMethod.construct(
            method, typenames, class_instantiations, method_instantiations,
            instantiated_args, parent)
        self.assertEqual(instantiated_method.name, "methodDouble")
        self.assertEqual(
            instantiated_method.args.list()[0].ctype.get_typename(), "double")

    def test_to_cpp(self):
        """Test the to_cpp method."""
        actual = self.method.to_cpp()
        self.assertEqual(actual, "method<double>")


class TestInstantiatedStaticMethod(unittest.TestCase):
    """Tests for the InstantiatedStaticMethod class."""
    def test_constructor(self):
        """Test constructor."""
        pass

    def test_construct(self):
        pass

    def test_to_cpp(self):
        pass


class TestInstantiatedClass(unittest.TestCase):
    """Tests for the InstantiatedClass class."""
    def test_constructor(self):
        """Test constructor."""
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
    def setUp(self):
        #TODO(Varun) Need to support templated class forward declaration.
        forward_declaration = ForwardDeclaration.rule.parseString("""
            class FooBar;
            """)[0]
        instantiations = [Typename.rule.parseString("double")[0]]
        self.declaration = InstantiatedDeclaration(
            forward_declaration, instantiations=instantiations)

    def test_constructor(self):
        """Test constructor."""
        self.assertIsInstance(self.declaration, InstantiatedDeclaration)
        self.assertIsInstance(self.declaration.original, ForwardDeclaration)
        self.assertEqual(self.declaration.instantiations[0].name, "double")

    def test_to_cpp(self):
        """Test to_cpp method."""
        cpp = self.declaration.to_cpp()
        self.assertEqual(cpp, "FooBar<double>")


class TestTemplateInstantiator(unittest.TestCase):
    """
    Test overall template instantiation and the functions in the module.
    """
    def test_scoped_template(self):
        """Test is_scoped_template."""
        # Test if not scoped template.
        template_typenames = ['T']
        str_arg_typename = "double"
        scoped_template, scoped_idx = is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertFalse(scoped_template)
        self.assertEqual(scoped_idx, -1)

        # Check for correct template match.
        template_typenames = ['T']
        str_arg_typename = "gtsam::Matrix"
        scoped_template, scoped_idx = is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertFalse(scoped_template)
        self.assertEqual(scoped_idx, -1)

        # Test scoped templatte
        template_typenames = ['T']
        str_arg_typename = "T::Value"
        scoped_template, scoped_idx = is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertEqual(scoped_template, "T")
        self.assertEqual(scoped_idx, 0)

        template_typenames = ['U', 'T']
        str_arg_typename = "T::Value"
        scoped_template, scoped_idx = is_scoped_template(
            template_typenames, str_arg_typename)
        self.assertEqual(scoped_template, "T")
        self.assertEqual(scoped_idx, 1)

    def test_instantiate_type(self):
        """Test for instantiate_type."""
        arg = Argument.rule.parseString("const T x")[0]
        template_typenames = ["T"]
        instantiations = [Typename.rule.parseString("double")[0]]
        cpp_typename = "ExampleClass"
        new_type = instantiate_type(arg.ctype,
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
        instantiated_args_list = instantiate_args_list(
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
        instantiated_args_list = instantiate_args_list(
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
        instantiated_args_list = instantiate_args_list(
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
        instantiated_return_type = instantiate_return_type(
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
        instantiated_return_type = instantiate_return_type(
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
        instantiated_name = instantiate_name("Iron", instantiations)
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
        instantiated_namespace = instantiate_namespace(namespace)

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
