"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Parser class and rules for parsing C++ enums.

Author: Varun Agrawal
"""

from pyparsing import Optional, alphas, delimitedList, pyparsing_common

from .tokens import ENUM, EQUAL, IDENT, LBRACE, RBRACE, SEMI_COLON
from .utils import collect_namespaces


class Enumerator:
    """
    Rule to parse an enumerator inside an enum.
    """
    rule = (IDENT("name") +
            Optional(EQUAL + (pyparsing_common.signed_integer ^ alphas))
            ).setParseAction(lambda t: Enumerator(t.name))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Enumerator: ({0})".format(self.name)


class Enum:
    """
    Rule to parse enums defined in the interface file.

    E.g.
    ```
    enum Kind {
        Dog = 0,
        Cat
    };
    ```
    """

    rule = (ENUM + IDENT("name") + LBRACE +
            delimitedList(Enumerator.rule)("enumerators") + RBRACE +
            SEMI_COLON).setParseAction(lambda t: Enum(t.name, t.enumerators))

    def __init__(self, name, enumerators, parent=''):
        self.name = name
        self.enumerators = enumerators
        self.parent = parent

    def namespaces(self) -> list:
        """Get the namespaces which this class is nested under as a list."""
        return collect_namespaces(self)
