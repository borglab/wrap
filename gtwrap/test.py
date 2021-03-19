from pyparsing import Group, OneOrMore, ParseResults, Literal, QuotedString, Suppress, Word, ZeroOrMore, delimitedList, alphanums, Char, LineEnd, ParserElement

import interface_parser as parser

test_string = """
import "linear/linear.i"

void func(int x);
void func2(int x);

import "slam/random.i"
"""

test2 = """
class Random{};

void func(int x);

class Discrete {};
"""

# PATH = QuotedString('"')
QUOTE = Suppress('"')
PATH = Word(alphanums + "./")
NL = Suppress(LineEnd())


class Import:
    rule = (Suppress("import") + QUOTE + PATH("path") + QUOTE +
            NL).setParseAction(lambda t: Import(t.path))

    rule.setDefaultWhitespaceChars(" \t")

    def __init__(self, path):
        # print("Import", path)
        self.path = path

    @staticmethod
    def parseString(s: str) -> ParseResults:
        """Parse the source string and apply the rules."""
        return Import.rule.parseString(s)

    def __repr__(self) -> str:
        return "Import({})".format(self.path)


class Statement:
    rule = Word(alphanums + " ();")


class Module:
    rule = ZeroOrMore(Import.rule ^ Statement.rule ^ NL)
    # rule.setDefaultWhitespaceChars(" \t")

    @staticmethod
    def parseString(s: str) -> ParseResults:
        """Parse the source string and apply the rules."""
        return Module.rule.parseString(s)


result = Module.parseString(test_string)
print(result)

# result = parser.Module.parseString(test2)
# print(result)
