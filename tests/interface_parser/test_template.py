import unittest

from gtwrap.interface_parser import Template, TypedefTemplateInstantiation


class TestTemplate(unittest.TestCase):
    """Unit tests for Template class."""

    def test_basic_template(self):
        """Test parsing of template."""
        template: Template = Template.rule.parseString(
            "template<POSE, CALIBRATION>")[0]
        self.assertListEqual(["POSE", "CALIBRATION"], template.names)
        self.assertListEqual([[], []], template.instantiations)

    def test_template_instantiations(self):
        """Test parsing of template."""
        template: Template = Template.rule.parse_string(
            "template<X = {double, float, int}, Y = {gtsam::Pose2, gtsam::Pose3}>"
        )[0]
        self.assertListEqual(["X", "Y"], template.names)
        self.assertListEqual(
            ["double", "float", "int"],
            [i.get_type() for i in template.instantiations[0]])

        self.assertListEqual(
            ["gtsam::Pose2", "gtsam::Pose3"],
            [i.get_type() for i in template.instantiations[1]])


class TestTypedefTemplateInstantiation(unittest.TestCase):
    """Unit tests for TypedefTemplateInstantiation."""

    def test_parsing(self):
        """Test for typedef'd instantiation of a template."""
        typedef = TypedefTemplateInstantiation.rule.parseString("""
        typedef gtsam::BearingFactor<gtsam::Pose2, gtsam::Point2, gtsam::Rot2>
            BearingFactor2D;
        """)[0]
        self.assertEqual("BearingFactor2D", typedef.new_name)
        self.assertEqual("BearingFactor", typedef.type.name)
        self.assertEqual(["gtsam"], typedef.type.namespaces)
        self.assertEqual(3, len(typedef.type.template_params))
        self.assertEqual(["gtsam"], typedef.type.namespaces)
