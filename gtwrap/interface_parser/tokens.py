"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

All the token definitions.

Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, and Frank Dellaert
"""

from pyparsing import (Keyword, Literal, Or, QuotedString, Suppress, Word,
                       ZeroOrMore, OneOrMore, alphanums, alphas, nestedExpr, nums,
                       originalTextFor, printables, pyparsing_common)

# rule for identifiers (e.g. variable names)
IDENT = Word(alphas + '_', alphanums + '_') ^ Word(nums)

RAW_POINTER, SHARED_POINTER, REF = map(Literal, "@*&")

LPAREN, RPAREN, LBRACE, RBRACE, COLON, SEMI_COLON = map(Suppress, "(){}:;")
LOPBRACK, ROPBRACK, COMMA, EQUAL = map(Suppress, "<>,=")

# Encapsulating type for numbers, and single and double quoted strings.
# The pyparsing_common utilities ensure correct coversion to the corresponding type.
# E.g. pyparsing_common.number will convert 3.1415 to a float type.
NUMBER_OR_STRING = (pyparsing_common.number
                    ^ QuotedString('"', unquoteResults=False)
                    ^ QuotedString("'", unquoteResults=False))

# Different types of high-level args
BASIC_ARG = Word(alphas + "{}:")
PARAMETERIZED_ARG = originalTextFor(Word(alphanums + ":") + nestedExpr())
TEMPLATED_ARG = originalTextFor(
    Word(printables, excludeChars='<') + Literal('<') +
    ZeroOrMore(Word(printables, excludeChars='>')) + Literal('>') +
    nestedExpr())
# Default argument passed to functions/methods.
DEFAULT_ARG = originalTextFor(
    OneOrMore(
        QuotedString('"') ^  #
        QuotedString("'") ^  #
        nestedExpr(opener='(', closer=')') ^  #
        nestedExpr(opener='[', closer=']') ^  #
        nestedExpr(opener='{', closer='}') ^  #
        nestedExpr(opener='<', closer='>') ^  #
        Word(printables, excludeChars="(){}[]<>,;")))

CONST, VIRTUAL, CLASS, STATIC, PAIR, TEMPLATE, TYPEDEF, INCLUDE = map(
    Keyword,
    [
        "const",
        "virtual",
        "class",
        "static",
        "pair",
        "template",
        "typedef",
        "#include",
    ],
)
ENUM = Keyword("enum") ^ Keyword("enum class") ^ Keyword("enum struct")
NAMESPACE = Keyword("namespace")
BASIS_TYPES = map(
    Keyword,
    [
        "void",
        "bool",
        "unsigned char",
        "char",
        "int",
        "size_t",
        "double",
        "float",
    ],
)

OPERATOR = Or(
    map(
        Literal,
        [
            '+',  # __add__, __pos__
            '-',  # __sub__, __neg__
            '*',  # __mul__
            '/',  # __truediv__
            '%',  # __mod__
            '^',  # __xor__
            '&',  # __and__
            '|',  # __or__
            # '~',  # __invert__
            '+=',  # __iadd__
            '-=',  # __isub__
            '*=',  # __imul__
            '/=',  # __itruediv__
            '%=',  # __imod__
            '^=',  # __ixor__
            '&=',  # __iand__
            '|=',  # __ior__
            '<<',  # __lshift__
            '<<=',  # __ilshift__
            '>>',  # __rshift__
            '>>=',  # __irshift__
            '==',  # __eq__
            '!=',  # __ne__
            '<',  # __lt__
            '>',  # __gt__
            '<=',  # __le__
            '>=',  # __ge__
            # '!',  # Use `not` in python
            # '&&',  # Use `and` in python
            # '||',  # Use `or` in python
            '()',  # __call__
            '[]',  # __getitem__
        ],
    ))
