import unittest

from gtwrap.interface_parser.enum import Enum, Enumerator


class TestEnum(unittest.TestCase):
    """Unit tests about Enum class."""

    def test_enumerator(self):
        """Test for enumerator."""
        enumerator = Enumerator.rule.parseString("Dog")[0]
        self.assertEqual(enumerator.name, "Dog")

        enumerator = Enumerator.rule.parseString("Cat")[0]
        self.assertEqual(enumerator.name, "Cat")

    def test_enum(self):
        """Test for enums."""
        enum = Enum.rule.parseString("""
        enum Kind {
            Dog,
            Cat
        };
        """)[0]
        self.assertEqual(enum.name, "Kind")
        self.assertEqual(enum.enumerators[0].name, "Dog")
        self.assertEqual(enum.enumerators[1].name, "Cat")
