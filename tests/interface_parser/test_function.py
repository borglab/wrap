import unittest

from gtwrap.interface_parser.function import (ArgumentList, GlobalFunction,
                                              ReturnType)


class TestArgument(unittest.TestCase):
    """Unit tests for the Argument class."""


class TestArgumentList(unittest.TestCase):
    """Unit tests for the ArgumentList class."""

    def test_empty_arguments(self):
        """Test no arguments."""
        empty_args = ArgumentList.rule.parseString("")[0]
        self.assertEqual(0, len(empty_args))

    def test_argument_list(self):
        """Test arguments list for a method/function."""
        arg_string = "int a, C1 c1, C2& c2, C3* c3, "\
            "const C4 c4, const C5& c5,"\
            "const C6* c6"
        args = ArgumentList.rule.parseString(arg_string)[0]

        self.assertEqual(7, len(args.list()))
        self.assertEqual(['a', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6'],
                         args.names())

    def test_argument_list_qualifiers(self):
        """
        Test arguments list where the arguments are qualified with `const`
        and can be either raw pointers, shared pointers or references.
        """
        arg_string = "double x1, double* x2, double& x3, double@ x4, " \
            "const double x5, const double* x6, const double& x7, const double@ x8"
        args = ArgumentList.rule.parseString(arg_string)[0].list()
        self.assertEqual(8, len(args))
        self.assertFalse(args[1].type.is_ptr and args[1].type.is_shared_ptr
                         and args[1].type.is_ref)
        self.assertTrue(args[1].type.is_shared_ptr)
        self.assertTrue(args[2].type.is_ref)
        self.assertTrue(args[3].type.is_ptr)
        self.assertTrue(args[4].type.is_const)
        self.assertTrue(args[5].type.is_shared_ptr and args[5].type.is_const)
        self.assertTrue(args[6].type.is_ref and args[6].type.is_const)
        self.assertTrue(args[7].type.is_ptr and args[7].type.is_const)

    def test_argument_list_templated(self):
        """Test arguments list where the arguments can be templated."""
        arg_string = "std::pair<string, double> steps, vector<T*> vector_of_pointers"
        args = ArgumentList.rule.parseString(arg_string)[0]
        args_list = args.list()
        self.assertEqual(2, len(args_list))
        self.assertEqual("std::pair<string, double>",
                         args_list[0].type.to_cpp())
        self.assertEqual("vector<std::shared_ptr<T>>",
                         args_list[1].type.to_cpp())

    def test_default_arguments(self):
        """Tests any expression that is a valid default argument"""
        args = ArgumentList.rule.parseString("""
            string c = "", int z = 0, double z2 = 0.0, bool f = false,
            string s="hello"+"goodbye", char c='a', int a=3,
            int b, double pi = 3.1415""")[0].list()

        # Test for basic types
        self.assertEqual(args[0].default_value, '""')
        self.assertEqual(args[1].default_value, '0')
        self.assertEqual(args[2].default_value, '0.0')
        self.assertEqual(args[3].default_value, "false")
        self.assertEqual(args[4].default_value, '"hello"+"goodbye"')
        self.assertEqual(args[5].default_value, "'a'")
        self.assertEqual(args[6].default_value, '3')
        # No default argument should set `default_value` to None
        self.assertIsNone(args[7].default_value)
        self.assertEqual(args[8].default_value, '3.1415')

        arg0 = 'gtsam::DefaultKeyFormatter'
        arg1 = 'std::vector<size_t>()'
        arg2 = '{1, 2}'
        arg3 = '[&c1, &c2](string s=5, int a){return s+"hello"+a+c1+c2;}'
        arg4 = 'gtsam::Pose3()'
        arg5 = 'Factor<gtsam::Pose3, gtsam::Point3>()'
        arg6 = 'gtsam::Point3(1, 2, 3)'
        arg7 = 'ns::Class<T, U>(3, 2, 1, "name")'

        argument_list = f"""
            gtsam::KeyFormatter kf = {arg0},
            std::vector<size_t> v = {arg1},
            std::vector<size_t> l = {arg2},
            gtsam::KeyFormatter lambda = {arg3},
            gtsam::Pose3 p = {arg4},
            Factor<gtsam::Pose3, gtsam::Point3> x = {arg5},
            gtsam::Point3 x = {arg6},
            ns::Class<T, U> obj = {arg7}
            """
        args = ArgumentList.rule.parseString(argument_list)[0].list()

        # Test non-basic type
        self.assertEqual(args[0].default_value, arg0)
        # Test templated type
        self.assertEqual(args[1].default_value, arg1)
        self.assertEqual(args[2].default_value, arg2)
        self.assertEqual(args[3].default_value, arg3)
        self.assertEqual(args[4].default_value, arg4)
        self.assertEqual(args[5].default_value, arg5)
        self.assertEqual(args[6].default_value, arg6)
        # Test for default argument with multiple templates and params
        self.assertEqual(args[7].default_value, arg7)


class TestReturnType(unittest.TestCase):
    """Unit tests for the ReturnType class."""

    def test_void_return_type(self):
        """Test void return type"""
        return_type = ReturnType.rule.parseString("void")[0]
        self.assertEqual("void", return_type.type1.name)
        self.assertTrue(return_type.type1.is_basic_type)

    def test_basic_return_type(self):
        """Test basic return type"""
        return_type = ReturnType.rule.parseString("size_t")[0]
        self.assertEqual("size_t", return_type.type1.name)
        self.assertTrue(not return_type.type2)
        self.assertTrue(return_type.type1.is_basic_type)

    def test_return_type_with_qualifiers(self):
        """Test return type with qualifiers such as const and `&`."""
        return_type = ReturnType.rule.parseString("int&")[0]
        self.assertEqual("int", return_type.type1.name)
        self.assertTrue(return_type.type1.is_basic_type
                        and return_type.type1.is_ref)

        return_type = ReturnType.rule.parseString("const int")[0]
        self.assertEqual("int", return_type.type1.name)
        self.assertTrue(return_type.type1.is_basic_type
                        and return_type.type1.is_const)

    def test_pair_return_type(self):
        """Test when return type is a std::pair."""
        return_type = ReturnType.rule.parseString("pair<char, int>")[0]
        self.assertEqual("char", return_type.type1.name)
        self.assertEqual("int", return_type.type2.name)

    def test_pair_return_type_qualifiers(self):
        """Test when return type is a std::pair and the types have qualifiers, e.g. * for shared pointer."""
        return_type = ReturnType.rule.parseString("pair<Test ,Test*>")[0]
        self.assertEqual("Test", return_type.type1.name)
        self.assertEqual("Test", return_type.type2.name)
        self.assertTrue(return_type.type2.is_shared_ptr)


class TestFunction(unittest.TestCase):
    """Unit tests for the GlobalFunction class."""

