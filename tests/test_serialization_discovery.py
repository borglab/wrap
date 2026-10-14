"""Selection uses instantiated declarations, without generating bindings."""
import unittest

from gtwrap.serialization import discover


class TestDiscovery(unittest.TestCase):
    SOURCE = '''namespace example {
class First { void serializable() const; };
class Second { void serialize() const; };
class Plain {};
}'''

    def test_sources_filters_and_exclusions(self):
        sources = [('one.i', self.SOURCE), ('two.i', self.SOURCE)]
        self.assertEqual([e.cpp_type for e in discover(sources)],
                         ['example::First', 'example::Second'])
        self.assertEqual([e.cpp_type for e in discover(
            sources, ['example::'], ['example::First'])], ['example::Second'])
        with self.assertRaisesRegex(ValueError, 'one.i.*no serializable'):
            discover(sources, ['other::'])
        with self.assertRaisesRegex(ValueError, 'end in ::'):
            discover(sources, ['example'])

    def test_template_alias_and_collision(self):
        source = '''namespace example {
template<A, B> class Pair {};
@serializable typedef example::Pair<int, double> PairID;
}'''
        entry, = discover([('alias.i', source)])
        self.assertEqual(entry.cpp_type, 'example::Pair<int, double>')
        self.assertEqual(entry.name, 'examplePairintdouble')
        collision = 'class examplePairintdouble { void serialize() const; };'
        with self.assertRaisesRegex(ValueError, 'collision.i.*alias.i'):
            discover([('alias.i', source), ('collision.i', collision)])
