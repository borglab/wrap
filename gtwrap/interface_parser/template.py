"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Classes and rules for parsing C++ templates and typedefs for template instantiations.

Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, and Frank Dellaert
"""

from typing import list

from pyparsing import DelimitedList, Optional, ParseResults  # type: ignore

from .tokens import (EQUAL, IDENT, LBRACE, LOPBRACK, RBRACE, ROPBRACK,
                     SEMI_COLON, TEMPLATE, TYPEDEF)
from .type import TemplatedType, Type


class TypenameAndInstantiations:
    """
        Rule to parse the template parameters.

        E.g. `template<POSE = {Pose2, Pose3}>`
        POSE is the typename and
        Pose2 and Pose3 are the `Instantiation`s.
        """
    rule = (
        IDENT("typename")  #
        + Optional(  #
            EQUAL  #
            + LBRACE  #
            +
            DelimitedList(TemplatedType.rule ^ Type.rule)("instantiations")  #
            + RBRACE  #
        )).setParseAction(
            lambda t: TypenameAndInstantiations(t.typename, t.instantiations))

    def __init__(self, typename: str, instantiations: ParseResults):
        self.typename = typename

        self.instantiations = []
        if instantiations:
            for inst in instantiations:
                x = inst.typename if isinstance(inst, TemplatedType) else inst
                self.instantiations.append(x)


class Template:
    """
    Rule to parse templated definition for a class/function in the interface file.

    E.g.
    template<POSE, CALIBRATION>  // this is the Template.
    class Camera { ... };
    """

    rule = (  # BR
        TEMPLATE  #
        + LOPBRACK  #
        + DelimitedList(TypenameAndInstantiations.rule)(
            "typename_and_instantiations")  #
        + ROPBRACK  # BR
    ).setParseAction(
        lambda t: Template(t.typename_and_instantiations.as_list()))

    def __init__(self,
                 typenames_and_instantiations: list[TypenameAndInstantiations]):
        ti_list = typenames_and_instantiations
        self.names = [ti.typename for ti in ti_list]
        self.instantiations = [ti.instantiations for ti in ti_list]

    def __repr__(self) -> str:
        return f"<{', '.join(self.names)}>"


class TypedefTemplateInstantiation:
    """
    Rule for parsing typedefs (with templates) within the interface file.

    E.g.
    ```
    typedef SuperComplexName<Arg1, Arg2, Arg3> EasierName;
    ```
    """
    rule = (TYPEDEF + TemplatedType.rule("templated_type") +
            IDENT("new_name") +
            SEMI_COLON).setParseAction(lambda t: TypedefTemplateInstantiation(
                t.templated_type[0], t.new_name))

    def __init__(self,
                 templated_type: TemplatedType,
                 new_name: str,
                 parent: str = ''):
        self.type = templated_type.type
        self.new_name = new_name
        self.parent = parent

    def __repr__(self):
        return f"Typedef: {self.new_name} = {self.type}"
