"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Parser classes and rules for parsing C++ variables.

Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, and Frank Dellaert
"""

from .tokens import IDENT, SEMI_COLON
from .type import TemplatedType, Type

class Variable:
    """
    Rule to parse the variable members of a class.

    E.g.
    ```
    class Hello {
        string name;  // This is a property.
    };
    ````
    """
    rule = (
        (Type.rule ^ TemplatedType.rule)("ctype")  #
        + IDENT("name")  #
        + SEMI_COLON  #
    ).setParseAction(lambda t: Variable(t.ctype, t.name))

    def __init__(self, ctype: Type, name: str, parent=''):
        self.ctype = ctype[0]  # ParseResult is a list
        self.name = name
        self.parent = parent

    def __repr__(self) -> str:
        return '{} {}'.format(self.ctype.__repr__(), self.name)
