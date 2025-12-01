"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Parser classes and rules for parsing C++ variables.

Author: Varun Agrawal, Gerry Chen
"""

from pyparsing import Optional, ParseResults  # type: ignore

from gtwrap.interface_parser.tokens import (DEFAULT_ARG, EQUAL, IDENT,
                                            SEMI_COLON)
from gtwrap.interface_parser.type import TemplatedType, Type


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
    rule = ((Type.rule ^ TemplatedType.rule)("type")  #
            + IDENT("name")  #
            + Optional(EQUAL + DEFAULT_ARG)("default_value")  #
            + SEMI_COLON  #
            ).setParseAction(lambda t: Variable(
                t.type[0],  #
                t.name,  #
                t.default_value[0]
                if isinstance(t.default_value, ParseResults) else None))

    def __init__(self,
                 t: Type,
                 name: str,
                 default_value: ParseResults = None,
                 parent=""):
        self.type = t
        self.name = name
        self.default_value = default_value
        self.parent = parent

    def __repr__(self) -> str:
        return f"{self.type} {self.name}"
