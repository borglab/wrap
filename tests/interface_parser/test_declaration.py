import unittest

from gtwrap.interface_parser.declaration import ForwardDeclaration, Include


class TestInclude(unittest.TestCase):
    """Unit tests for Include class."""

    def test_parsing(self):
        """Test for include statements."""
        include = Include.rule.parseString(
            "#include <gtsam/slam/PriorFactor.h>")[0]
        self.assertEqual("gtsam/slam/PriorFactor.h", include.header)


class TestForwardDeclaration(unittest.TestCase):
    """Unit tests for ForwardDeclaration class."""

    def test_parsing(self):
        """Test for forward declarations."""
        fwd = ForwardDeclaration.rule.parseString(
            "virtual class Test:gtsam::Point3;")[0]

        self.assertEqual("Test", fwd.name)
        self.assertTrue(fwd.is_virtual)
