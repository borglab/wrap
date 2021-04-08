"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

All the token definitions.

Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, and Frank Dellaert
"""

from pyparsing import Keyword, Literal, Suppress, Word, alphanums, alphas, nums, Or, removeQuotes, \
                      quotedString, originalTextFor, OneOrMore, Word, printables, nestedExpr

# punctuation and basic elements
LPAR,RPAR = map(Suppress, "()")

# rule for identifiers (e.g. variable names)
IDENT = Word(alphas + '_', alphanums + '_') ^ Word(nums)
# rule for expressions (e.g. default arguments).
# This can't really be truly syntax checked so instead just allow almost everything until delimiters
# see https://stackoverflow.com/a/40688583/9151520
EXPRESSION = (quotedString
              | originalTextFor(OneOrMore(Word(printables, excludeChars="(),")
                                          | nestedExpr())))

RAW_POINTER, SHARED_POINTER, REF = map(Literal, "@*&")

LPAREN, RPAREN, LBRACE, RBRACE, COLON, SEMI_COLON = map(Suppress, "(){}:;")
LOPBRACK, ROPBRACK, COMMA, EQUAL = map(Suppress, "<>,=")
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
