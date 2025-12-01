"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Define the parser rules and classes for various C++ types.

Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, and Frank Dellaert
"""

# pylint: disable=unnecessary-lambda, expression-not-assigned

from pyparsing import ParseResults  # type: ignore
from pyparsing import DelimitedList, Forward, Optional, Or

from .tokens import (BASIC_TYPES, CONST, IDENT, LOPBRACK, RAW_POINTER, REF,
                     ROPBRACK, SHARED_POINTER)


class Typename:

    def instantiated_name(self) -> str:
        """Get the instantiated name of the type."""
        res = self.name
        for instantiation in self.instantiations:
            res += instantiation.instantiated_name()
        return res

    def __eq__(self, other) -> bool:
        if isinstance(other, Typename):
            return str(self) == str(other)
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


class Type:
    """
    Parsed variable with type, which can be either a fundamental/basic type or a custom datatype.
    E.g. void, double, size_t, Matrix.

    The variable can optionally be a raw pointer, shared pointer or reference.
    Can also be optionally qualified with a `const`, e.g. `const int`.
    """

    @staticmethod
    def from_parsed_result(t: ParseResults):
        """Return the resulting Type from parsing the source."""
        # If the type is a basic/fundamental c++ type (e.g int, bool)
        if t.basic:
            name = t.basic
            namespaces = []
            is_basic_type = True
        elif t.custom:
            name = t.custom[-1]
            namespaces = t.custom[:-1]
            is_basic_type = False
        else:
            raise ValueError("Parse result is not a Type")

        return Type(
            name=name,
            namespaces=namespaces,
            is_const=t.is_const,
            is_shared_ptr=t.is_shared_ptr,
            is_ptr=t.is_ptr,
            is_ref=t.is_ref,
            is_basic_type=is_basic_type,
        )

    @staticmethod
    def basic_type_rule():
        """
        Basic types are the fundamental built-in types in C++ such as double, int, char, etc.
        When using templates, the basic type will take on the same form as the template.

        E.g.
        ```
        template<T = {double}>
        void func(const T& x);
        ```

        will give

        ```
        m_.def("funcDouble",[](const double& x){
            ::func<double>(x);
        }, py::arg("x"));
        ```
        """
        return Or(BASIC_TYPES)

    @staticmethod
    def custom_type_rule():
        """
        Custom defined types with the namespace.
        Essentially any C++ data type that is not a BasicType.

        E.g.
        ```
        gtsam::Matrix wTc;
        ```

        Here `gtsam::Matrix` is a custom type.
        """
        return DelimitedList(IDENT, "::")

    rule = (
        Optional(CONST("is_const"))  #
        + (basic_type_rule()("basic") | custom_type_rule()("custom"))  #
        + Optional(
            SHARED_POINTER("is_shared_ptr") | RAW_POINTER("is_ptr")
            | REF("is_ref"))  #
    ).setParseAction(from_parsed_result)

    def __init__(self, name: str, namespaces: list[str], is_const: str,
                 is_shared_ptr: str, is_ptr: str, is_ref: str,
                 is_basic_type: bool):
        self.name = name
        self.namespaces = namespaces
        # If the first namespace is empty string, just get rid of it.
        if self.namespaces and self.namespaces[0] == '':
            self.namespaces.pop(0)

        self.is_const = is_const
        self.is_shared_ptr = is_shared_ptr
        self.is_ptr = is_ptr
        self.is_ref = is_ref
        self.is_basic_type = is_basic_type

    def __repr__(self) -> str:
        is_ptr_or_ref = f"{self.is_shared_ptr}{self.is_ptr}{self.is_ref}"
        const_str = "const " if self.is_const else ""
        return f"Type: {const_str}{self.get_type()}{' ' + is_ptr_or_ref if is_ptr_or_ref else ''}"

    def get_type(self):
        """
        Get the fully qualified typename, i.e. the type name with all of its namespaces.
        E.g. for `const gtsam::internal::Pose3& pose` this will return `gtsam::internal::Pose3`.
        """
        return "::".join(self.namespaces + [self.name])

    def to_cpp(self) -> str:
        """
        Generate the C++ code for wrapping.

        Treat all pointers as "const shared_ptr<T>&"
        """

        if self.is_shared_ptr:
            type_value = f"std::shared_ptr<{self.get_type()}>"
        elif self.is_ptr:
            type_value = f"{self.get_type()}*"
        elif self.is_ref:
            type_value = f"{self.get_type()}&"
        else:
            type_value = self.get_type()

        const = "const " if self.is_const else ""
        return f"{const}{type_value}"


class TemplatedType(Type):
    """
    Type which is templated.
    This is done so that the template parameters can be pointers/references.

    E.g. std::vector<double>, BearingRange<Pose3, Point3&>
    """

    @staticmethod
    def from_parsed_result(t: ParseResults):
        """Get the TemplatedType from the parser results."""
        name = t.type.name
        namespaces = t.type.namespaces
        is_basic_type = t.type.is_basic_type

        return TemplatedType(name, namespaces, t.template_params.as_list(),
                             t.is_const, t.is_shared_ptr, t.is_ptr, t.is_ref,
                             is_basic_type)

    rule = Forward()
    rule << (
        Optional(CONST("is_const"))  #
        + Type.rule("type")  #
        + (
            LOPBRACK  #
            + DelimitedList(Type.rule ^ rule, ",")("template_params")  #
            + ROPBRACK)  #
        + Optional(
            SHARED_POINTER("is_shared_ptr") | RAW_POINTER("is_ptr")
            | REF("is_ref"))  #
    ).setParseAction(from_parsed_result)

    def __init__(self, name: str, namespaces: list[str],
                 template_params: list[Type], is_const: str,
                 is_shared_ptr: str, is_ptr: str, is_ref: str,
                 is_basic_type: bool):
        super().__init__(name,
                         namespaces,
                         is_const=is_const,
                         is_shared_ptr=is_shared_ptr,
                         is_ptr=is_ptr,
                         is_ref=is_ref,
                         is_basic_type=is_basic_type)

        self.template_params = template_params

    def __repr__(self):
        return f"TemplatedType({self.namespaces}::{self.name}<{self.template_params}>)"

    def get_template_params(self):
        """
        Get the template args for the type as a string.
        E.g. for
            ```
            template <T = {double}, U = {string}>
            class Random(){};
            ```
        it returns `<double, string>`.

        """
        # Use Type.to_cpp to do the heavy lifting for the template parameters.
        return ", ".join([t.to_cpp() for t in self.template_params])

    def get_type(self):
        """
        Get the typename of this type without any qualifiers.
        E.g. for `const std::vector<double>& indices` this will return `std::vector<double>`.
        """
        return f"{super().get_type()}<{self.get_template_params()}>"

    def templated_name(self) -> str:
        """Return the name without namespace and with the template instantiations."""
        templates = self.get_template_params()
        return f"{self.name}<{templates}>"

    def to_cpp(self):
        """
        Generate the C++ code for wrapping.
        """
        typename = self.get_type()

        if self.is_shared_ptr:
            typename = f"std::shared_ptr<{typename}>"
        elif self.is_ptr:
            typename = f"{typename}*"
        elif self.is_ref:
            typename = f"{typename}&"

        const = "const " if self.is_const else ""
        return f"{const}{typename}"
