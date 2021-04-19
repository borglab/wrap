"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Parser classes and rules for parsing C++ variables.

Author: Varun Agrawal, Gerry Chen
"""

from .tokens import IDENT, SEMI_COLON
from .type import TemplatedType, Type

class Variable:
    """
    Rule to parse variables.
    Variables are a combination of Type/TemplatedType and the variable identifier.

    E.g.
    ```
    class Hello {
        string name;  // This is a property variable.
    };

    Vector3 kGravity;  // This is a global variable.
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
