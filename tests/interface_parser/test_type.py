"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Tests for interface_parser.

Author: Varun Agrawal
"""
# pylint: disable=import-error,wrong-import-position

import os
import sys
import unittest

from gtwrap.interface_parser import TemplatedType, Type

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestType(unittest.TestCase):
    """Tests for the Type class."""

    def test_parsing(self):
        """Test parsing of Type."""
        t = Type.rule.parseString("size_t")[0]
        self.assertEqual("size_t", t.name)

    def test_parsing_with_namespaces(self):
        """Test parsing of Type with namespaces."""
        t = Type.rule.parseString("module_a::module_b::module_c::xyz")[0]
        self.assertEqual("xyz", t.name)
        self.assertListEqual(["module_a", "module_b", "module_c"],
                             t.namespaces)

    def test_basic_type_parsing(self):
        """Check basic type"""
        basic_types = [
            "void",
            "bool",
            "unsigned char",
            "char",
            "int",
            "size_t",
            "double",
            "float",
        ]
        for basic_type in basic_types:
            t = Type.rule.parseString(basic_type)[0]
            self.assertEqual(basic_type, t.name)
            self.assertTrue(t.is_basic_type)

    def test_custom_type_parsing(self):
        """Check custom type"""
        t = Type.rule.parseString("gtsam::Matrix")[0]
        self.assertEqual("Matrix", t.name)
        self.assertEqual(["gtsam"], t.namespaces)

    def test_qualified_name(self):
        """Test the qualified_name method."""
        variable_type: Type = Type.rule.parseString(
            "module_a::module_b::module_c::xyz")[0]
        self.assertEqual("module_a::module_b::module_c::xyz",
                         variable_type.get_type())

    def test_basic_const(self):
        """Check const."""
        t = Type.rule.parseString("const int x")[0]
        self.assertEqual("int", t.name)
        self.assertTrue(t.is_basic_type)
        self.assertTrue(t.is_const)

    def test_basic_shared_pointer(self):
        """Check shared pointer"""
        t = Type.rule.parseString("int* x")[0]
        self.assertEqual("int", t.name)
        self.assertTrue(t.is_shared_ptr)

    def test_basic_raw_pointer(self):
        """Check raw pointer"""
        t = Type.rule.parseString("int@ x")[0]
        self.assertEqual("int", t.name)
        self.assertTrue(t.is_ptr)

    def test_basic_reference(self):
        """Check reference"""
        t = Type.rule.parseString("int& x")[0]
        self.assertEqual("int", t.name)
        self.assertTrue(t.is_ref)

    def test_basic_const_reference(self):
        """Check const reference."""
        t = Type.rule.parseString("const int& x")[0]
        self.assertEqual("int", t.name)
        self.assertTrue(t.is_const)
        self.assertTrue(t.is_ref)

    def test_custom_type(self):
        """Test for CustomType."""
        # Check qualified type
        t = Type.rule.parseString("gtsam::Pose3 x")[0]
        self.assertEqual("Pose3", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertTrue(not t.is_basic_type)

    def test_custom_const(self):
        """Check const."""
        t = Type.rule.parseString("const gtsam::Pose3 x")[0]
        self.assertEqual("Pose3", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertTrue(t.is_const)

    def test_custom_shared_pointer(self):
        """Check shared pointer."""
        t = Type.rule.parseString("gtsam::Pose3* x")[0]
        self.assertEqual("Pose3", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertTrue(t.is_shared_ptr)
        self.assertEqual("std::shared_ptr<gtsam::Pose3>", t.to_cpp())

    def test_custom_raw_pointer(self):
        """Check raw pointer."""
        t = Type.rule.parseString("gtsam::Pose3@ x")[0]
        self.assertEqual("Pose3", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertTrue(t.is_ptr)

    def test_custom_reference(self):
        """Check reference."""
        t = Type.rule.parseString("gtsam::Pose3& x")[0]
        self.assertEqual("Pose3", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertTrue(t.is_ref)

    def test_custom_const_reference(self):
        """Check const reference."""
        t = Type.rule.parseString("const gtsam::Pose3& x")[0]
        self.assertEqual("Pose3", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertTrue(t.is_const)
        self.assertTrue(t.is_ref)

    # def test_parsing_templates(self):
    #     """Test parsing of Type with a template parameter."""


class TestTemplatedType(unittest.TestCase):
    """Unit tests for the TemplatedType class."""

    def test_templated_type(self):
        """Test a templated type."""
        t = TemplatedType.rule.parseString("Eigen::Matrix<double, 3, 4>")[0]
        self.assertEqual("Matrix", t.name)
        self.assertEqual(["Eigen"], t.namespaces)
        self.assertEqual("double", t.template_params[0].name)
        self.assertEqual("3", t.template_params[1].name)
        self.assertEqual("4", t.template_params[2].name)

        t = TemplatedType.rule.parseString(
            "gtsam::PinholeCamera<gtsam::Cal3S2>")[0]
        self.assertEqual("PinholeCamera", t.name)
        self.assertEqual(["gtsam"], t.namespaces)
        self.assertEqual("Cal3S2", t.template_params[0].name)
        self.assertEqual(["gtsam"], t.template_params[0].namespaces)

        t = TemplatedType.rule.parseString("PinholeCamera<Cal3S2*>")[0]
        self.assertEqual("PinholeCamera", t.name)
        self.assertEqual("Cal3S2", t.template_params[0].name)
        self.assertTrue(t.template_params[0].is_shared_ptr)
        self.assertTrue(t.template_params[0].is_shared_ptr)

    def test_template_within_template(self):
        t = TemplatedType.rule.parseString("gtsam::Data<std::vector<double>, uint64_t>")[0]
        print(t)
        