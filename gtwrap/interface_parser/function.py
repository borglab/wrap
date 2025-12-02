"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Parser classes and rules for parsing C++ functions.

Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, and Frank Dellaert
"""

from typing import Any, Union

from pyparsing import DelimitedList, Literal, Optional, ParseResults

from .template import Template
from .tokens import (COMMA, DEFAULT_ARG, EQUAL, IDENT, LOPBRACK, LPAREN, PAIR,
                     ROPBRACK, RPAREN, SEMI_COLON)
from .type import TemplatedType, Type


class Argument:
    """
    The type and name of a function/method argument.

    E.g.
    ```
    void sayHello(/*`s` is the method argument with type `const string&`*/ const string& s);
    ```
    """
    rule = ((Type.rule ^ TemplatedType.rule)("type")  #
            + IDENT("name")  #
            + Optional(EQUAL + DEFAULT_ARG)("default")).setParseAction(
                lambda t: Argument(
                    t.type[0], t.name, t.default[0]
                    if isinstance(t.default, ParseResults) else None), )

    def __init__(self,
                 t: Type | TemplatedType,
                 name: str,
                 default: ParseResults = None):

        self.type = t
        self.name = name
        self.default_value = default
        self.parent: ArgumentList | None = None

    def __repr__(self) -> str:
        return self.to_cpp()

    def to_cpp(self) -> str:
        """Return full C++ representation of argument."""
        return f"{self.type.to_cpp()} {self.name}"


class ArgumentList:
    """
    List of Argument objects for all arguments in a function.
    """

    # Rule which parses and directly returns the ParseResults
    # To be used when ArgumentList.rule is part of a larger rule, so we can use __getitem__
    rule_without_parse_action = Optional(
        DelimitedList(Argument.rule)("args_list"))

    @staticmethod
    def from_parsed_results(t: ParseResults):
        return ArgumentList(t)

    # Rule to parse arguments list and return an ArgumentList object
    rule = Optional(DelimitedList(
        Argument.rule)("args_list")).set_parse_action(from_parsed_results)

    def __init__(self, args_list: ParseResults):
        if args_list:
            if isinstance(args_list, ParseResults):
                self.args_list = args_list.as_list()
            else:
                self.args_list = args_list
        else:
            self.args_list = []

        for arg in args_list:
            arg.parent = self
        # The parent object which contains the argument list
        # E.g. Method, StaticMethod, Template, Constructor, GlobalFunction
        self.parent: Any = None

    def __repr__(self) -> str:
        return ", ".join([repr(x) for x in self.args_list])

    def __len__(self) -> int:
        return len(self.args_list)

    def __getitem__(self, i):
        return self.args_list[i]

    def names(self) -> list[str]:
        """Return a list of the names of all the arguments."""
        return [arg.name for arg in self.args_list]

    def to_cpp(self) -> list[str]:
        """Generate the C++ code for wrapping."""
        return [arg.type.to_cpp() for arg in self.args_list]


class ReturnType:
    """
    Rule to parse the return type.

    The return type can either be a single type or a pair such as <type1, type2>.
    """
    # rule to parse optional std:: in front of `pair`
    optional_std = Optional(Literal('std::')).suppress()
    _pair = (
        optional_std + PAIR.suppress()  #
        + LOPBRACK  #
        + Type.rule("type1")  #
        + COMMA  #
        + Type.rule("type2")  #
        + ROPBRACK  #
    )
    rule = (_pair ^
            (Type.rule ^ TemplatedType.rule)("type1")).setParseAction(  # BR
                lambda t: ReturnType(t.type1, t.type2))

    def __init__(self, type1: Union[Type, TemplatedType], type2: Type):
        # If a TemplatedType, the return is a ParseResults, so we extract out the type.
        self.type1 = type1[0] if isinstance(type1, ParseResults) else type1
        self.type2 = type2
        # The parent object which contains the return type
        # E.g. Method, StaticMethod, Template, Constructor, GlobalFunction
        self.parent: Any = None

    def is_void(self) -> bool:
        """
        Check if the return type is void.
        """
        return self.type1.typename.name == "void" and not self.type2

    def __repr__(self) -> str:
        return f"{self.type1}{', ' + self.type2 if self.type2 else ''}"

    def to_cpp(self) -> str:
        """
        Generate the C++ code for wrapping.

        If there are two return types, we return a pair<>,
        otherwise we return the regular return type.
        """
        if self.type2:
            return f"std::pair<{self.type1.to_cpp()},{self.type2.to_cpp()}>"
        else:
            return self.type1.to_cpp()


class GlobalFunction:
    """
    Rule to parse functions defined in the global scope.
    """
    rule = (
        Optional(Template.rule("template")) + ReturnType.rule("return_type")  #
        + IDENT("name")  #
        + LPAREN  #
        + ArgumentList.rule_without_parse_action("args_list")  #
        + RPAREN  #
        + SEMI_COLON  #
    ).setParseAction(lambda t: GlobalFunction(
        t.name,
        t.return_type,
        ArgumentList(t.args_list),
        t.template,
    ))

    def __init__(self,
                 name: str,
                 return_type: ReturnType,
                 args_list: ArgumentList,
                 template: Template,
                 parent: Any = ''):
        self.name = name
        self.return_type = return_type
        self.args = args_list
        self.template = template

        self.parent = parent
        self.return_type.parent = self
        self.args.parent = self

    def __repr__(self) -> str:
        return f"GlobalFunction:  {self.name}({self.args}) -> {self.return_type}"

    def to_cpp(self) -> str:
        """Generate the C++ code for wrapping."""
        return self.name
