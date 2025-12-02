"""Instantiate a class and its members."""

import gtwrap.interface_parser as parser
from gtwrap.template_instantiator.constructor import InstantiatedConstructor
from gtwrap.template_instantiator.helpers import (InstantiatedMember,
                                                  InstantiationHelper,
                                                  instantiate_args_list,
                                                  instantiate_name,
                                                  instantiate_return_type,
                                                  instantiate_type)
from gtwrap.template_instantiator.method import (InstantiatedMethod,
                                                 InstantiatedStaticMethod)


class InstantiatedClass(parser.Class):
    """
    Instantiate the class defined in the interface file.
    """

    def __init__(self, original: parser.Class, instantiations=(), new_name=''):
        """
        Template <T, U>
        Instantiations: [T1, U1]
        """
        self.original = original
        self.instantiations = instantiations

        self.template = None
        self.is_virtual = original.is_virtual
        self.parent = original.parent

        # If the class is templated, check if the number of provided instantiations
        # match the number of templates, else it's only a partial instantiation which is bad.
        if original.template:
            assert len(original.template.names) == len(
                instantiations), "Types and instantiations mismatch!"

        # Get the instantiated name of the class. E.g. FuncDouble
        self.name = instantiate_name(
            original.name, instantiations) if not new_name else new_name

        # Check for template type names if templated.
        # By passing in type names, we can gracefully handle both templated and non-templated classes
        # This will allow the `This` keyword to be used in both templated and non-templated classes.
        template_names = self.original.template.names if self.original.template else []

        # Instantiate the parent class, constructors, static methods, properties, respectively.
        self.parent_class = self.instantiate_parent_class(template_names)
        self.ctors = self.instantiate_ctors(template_names)
        self.static_methods = self.instantiate_static_methods(template_names)
        self.properties = self.instantiate_properties(template_names)

        # Instantiate all operator overloads
        self.operators = self.instantiate_operators(template_names)

        # Set enums
        self.enums = original.enums

        # Instantiate all instance methods
        self.methods = self.instantiate_methods(template_names)

        self.dunder_methods = original.dunder_methods

        super().__init__(
            self.template,
            self.is_virtual,
            self.name,
            [self.parent_class],
            self.ctors,
            self.methods,
            self.static_methods,
            self.dunder_methods,
            self.properties,
            self.operators,
            self.enums,
            parent=self.parent,
        )

    def __repr__(self):
        virtual = "virtual " if self.is_virtual else ''
        cpp_class = self.to_cpp()
        parent_class = self.parent
        ctors = "\n".join([repr(ctor) for ctor in self.ctors])
        static_methods = "\n".join([repr(m) for m in self.static_methods])
        methods = "\n".join([repr(m) for m in self.methods])
        operators = "\n".join([repr(op) for op in self.operators])

        return f"{virtual}Class {cpp_class} : {parent_class}\n{ctors}\n{static_methods}\n{methods}\n{operators}"

    def instantiate_parent_class(self, template_types):
        """
        Instantiate the inherited parent names.

        Args:
            template_types: List of template types to instantiate.

        Return: List of constructors instantiated with provided template args.
        """

        if isinstance(self.original.parent_class, parser.type.TemplatedType):
            parent_class = self.original.parent_class
            namespaces = self.namespaces()
            # Create the type which will be assigned as the parent of `parent_class`
            parent_type = parser.Type(name=namespaces[-1],
                                      namespaces=namespaces[:-1],
                                      is_const='',
                                      is_shared_ptr='',
                                      is_ptr='',
                                      is_ref='',
                                      is_basic_type='')
            return instantiate_type(parent_class, template_types,
                                    self.instantiations, parent_type)
        else:
            return self.original.parent_class

    def instantiate_ctors(self, template_params):
        """
        Instantiate the class constructors.

        Args:
            template_params: List of template types to instantiate, e.g. ['T', 'POSE'].

        Return: List of constructors instantiated with provided template args.
        """

        helper = InstantiationHelper(
            instantiation_type=InstantiatedConstructor)

        instantiated_ctors = helper.multilevel_instantiation(
            self.original.ctors, template_params, self)

        return instantiated_ctors

    def instantiate_static_methods(self, template_params):
        """
        Instantiate static methods in the class.

        Args:
            template_params: List of template types to instantiate, e.g. ['T', 'POSE'].

        Return: List of static methods instantiated with provided template args.
        """
        helper = InstantiationHelper(
            instantiation_type=InstantiatedStaticMethod)

        instantiated_static_methods = helper.multilevel_instantiation(
            self.original.static_methods, template_params, self)

        return instantiated_static_methods

    def instantiate_methods(self, template_params) -> list[InstantiatedMember]:
        """
        Instantiate regular methods in the class.

        Args:
            template_params: List of template parameters to instantiate, e.g. ['T', 'POSE'].

        Return: List of methods instantiated with provided template args.
        """
        instantiated_methods = []

        helper = InstantiationHelper(instantiation_type=InstantiatedMethod)

        instantiated_methods = helper.multilevel_instantiation(
            self.original.methods, template_params, self)

        return instantiated_methods

    def instantiate_operators(self, template_params):
        """
        Instantiate the class-level template in the operator overload.

        Args:
            template_params: List of template types to instantiate, e.g. ['T', 'POSE'].

        Return: List of methods instantiated with provided template args on the class.
        """
        instantiated_operators = []
        for operator in self.original.operators:
            instantiated_args = instantiate_args_list(
                operator.args,
                template_params,
                self.instantiations,
                self.cpp_type(),
            )
            instantiated_operators.append(
                parser.Operator(
                    name=operator.name,
                    operator=operator.operator,
                    return_type=instantiate_return_type(
                        operator.return_type,
                        template_params,
                        self.instantiations,
                        self.cpp_type(),
                    ),
                    args=parser.ArgumentList(instantiated_args),
                    is_const=operator.is_const,
                    parent=self,
                ))
        return instantiated_operators

    def instantiate_properties(self, template_params):
        """
        Instantiate the class properties.

        Args:
            template_params: List of template types to instantiate.

        Return: List of properties instantiated with provided template args.
        """
        instantiated_: list[parser.Argument] = instantiate_args_list(
            self.original.properties,
            template_params,
            self.instantiations,
            self.cpp_type(),
        )
        # Convert to type Variable
        instantiated_properties = [
            parser.Variable(t=arg.type,
                            name=arg.name,
                            default_value=arg.default_value) for arg in instantiated_
        ]
        return instantiated_properties

    def cpp_type(self):
        """
        Return a parser.Type including namespaces and cpp name of this
        class.
        """
        if self.original.template:
            instantiations = ", ".join([inst.to_cpp() for inst in self.instantiations])
            name = f"{self.original.name}<{instantiations}>"
        else:
            name = self.original.name

        return parser.Type(name=name,
                           namespaces=self.namespaces(),
                           is_const="",
                           is_shared_ptr="",
                           is_ptr="",
                           is_ref="",
                           is_basic_type="")

    def to_cpp(self):
        """Generate the C++ code for wrapping."""
        return self.cpp_type().to_cpp()
