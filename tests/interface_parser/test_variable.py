import unittest

from gtwrap.interface_parser.variable import Variable


class TestVariable(unittest.TestCase):
    """Unit tests for Variable class."""

    def test_global_variable(self):
        """Test for global variable."""
        variable: Variable = Variable.rule.parseString("string kGravity;")[0]
        self.assertEqual(variable.name, "kGravity")
        self.assertEqual(variable.type.name, "string")

        variable: Variable = Variable.rule.parseString(
            "string kGravity = 9.81;")[0]
        self.assertEqual(variable.name, "kGravity")
        self.assertEqual(variable.type.name, "string")
        self.assertEqual(variable.default_value, "9.81")

        variable: Variable = Variable.rule.parseString(
            "const string kGravity = 9.81;")[0]
        self.assertEqual(variable.name, "kGravity")
        self.assertEqual(variable.type.name, "string")
        self.assertTrue(variable.type.is_const)
        self.assertEqual(variable.default_value, "9.81")

        variable: Variable = Variable.rule.parseString(
            "gtsam::Pose3 wTc = gtsam::Pose3();")[0]
        self.assertEqual(variable.name, "wTc")
        self.assertEqual(variable.type.name, "Pose3")
        self.assertEqual(variable.default_value, "gtsam::Pose3()")

        variable: Variable = Variable.rule.parseString(
            "gtsam::Pose3 wTc = gtsam::Pose3(1, 2, 0);")[0]
        self.assertEqual(variable.name, "wTc")
        self.assertEqual(variable.type.name, "Pose3")
        self.assertEqual(variable.default_value, "gtsam::Pose3(1, 2, 0)")
