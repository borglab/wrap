"""Instantiate a forward declaration."""

import gtwrap.interface_parser as parser
from gtwrap.template_instantiator.helpers import instantiate_name


class InstantiatedDeclaration(parser.ForwardDeclaration):
    """
    Instantiate typedefs of forward declarations.
    This is useful when we wish to typedef a templated class
    which is not defined in the current project.

    E.g.
        class FactorFromAnotherMother;

        typedef FactorFromAnotherMother<gtsam::Pose3> FactorWeCanUse;
    """

    def __init__(self, original, instantiations=(), new_name=''):
        super().__init__(original.typename,
                         original.parent_type,
                         original.is_virtual,
                         parent=original.parent)

        self.original = original
        self.instantiations = instantiations
        self.parent = original.parent

        self.name = instantiate_name(
            original.name, instantiations) if not new_name else new_name

    def to_cpp(self):
        """Generate the C++ code for wrapping."""
        if namespace := "::".join(self.namespaces()):
            namespace += "::"

        instantiated_names = [inst.get_type() for inst in self.instantiations]

        return f"{namespace}{self.original.name}<{','.join(instantiated_names)}>"

    def __repr__(self):
        return f"Instantiated {super(InstantiatedDeclaration, self)}"
