"""Various helpers for instantiation."""

import itertools
from copy import deepcopy
from typing import Sequence, Union

import gtwrap.interface_parser as parser

ClassMember = Union[parser.Constructor, parser.Method, parser.StaticMethod,
                    parser.GlobalFunction, parser.Operator, parser.Variable,
                    parser.Enum]
InstantiatedMember = Union['InstantiatedConstructor', 'InstantiatedMethod',
                           'InstantiatedStaticMethod',
                           'InstantiatedGlobalFunction']


def is_scoped_template(templates: Sequence[str], str_arg_typename: str):
    """
    Check if the template given by `str_arg_typename` is a scoped template e.g. T::Value,
    and if so, return what template from `templates` and
    the corresponding index matches the scoped template correctly.
    """
    for idx, template in enumerate(templates):
        if "::" in str_arg_typename and \
            template in str_arg_typename.split("::"):
            return template, idx
    return False, -1


def instantiate_type(
        orignal_type: parser.Type,
        templates: Sequence[str],
        instantiations: Sequence[parser.Type],
        cpp_type: parser.Type,
        instantiated_class: 'InstantiatedClass' = None) -> parser.Type:
    """
    Instantiate template type for `orignal_type`.

    Args:
        orignal_type: The original argument type.
        templates: List of strings representing the templates.
        instantiations: List of the instantiations of the templates in `templates`.
        cpp_type: Full-namespace cpp class name of this instantiation
            to replace for arguments of type named `This`.
        instiated_class: The instantiated class which, if provided,
            will be used for instantiating `This`.

    Returns:
        If `orignal_type`'s name is in the `templates`, return the
        corresponding type to replace in `instantiations`.
        If orignal_type name is `This`, return the new typename `cpp_type`.
        Otherwise, return the original orignal_type.
    """
    # make a deep copy so that there is no overwriting of original template params
    ctype = deepcopy(orignal_type)

    # Check if the return type has template parameters as the typename's name
    if hasattr(ctype, 'template_params'):
        for idx, template_param in enumerate(ctype.template_params):
            if template_param.name in templates:
                template_idx = templates.index(template_param.name)
                ctype.template_param[idx].name =\
                    instantiations[template_idx]

    str_arg_type = str(ctype.get_type())

    # Check if template is a scoped template e.g. T::Value where T is the template
    scoped_template, scoped_idx = is_scoped_template(templates, str_arg_type)

    # Instantiate templates which have enumerated instantiations in the template.
    # E.g. `template<T={double}>`.

    # Instantiate scoped templates, e.g. T::Value.
    if scoped_template:
        # Create a copy of the instantiation so we can modify it.
        instantiation = deepcopy(instantiations[scoped_idx])

        # Replace the part of the template with the instantiation
        # This new typename has the updated name, previous namespaces and no instantiations
        return parser.Type(
            name=str_arg_type.replace(scoped_template,
                                      instantiation.templated_name()),
            namespaces=instantiation.namespaces,
            is_const=ctype.is_const,
            is_shared_ptr=ctype.is_shared_ptr,
            is_ptr=ctype.is_ptr,
            is_ref=ctype.is_ref,
            is_basic_type=ctype.is_basic_type,
        )

    # Check for exact template match.
    elif str_arg_type in templates:
        idx = templates.index(str_arg_type)
        return parser.Type(
            name=instantiations[idx].name,
            namespaces=instantiations[idx].namespaces,
            is_const=ctype.is_const,
            is_shared_ptr=ctype.is_shared_ptr,
            is_ptr=ctype.is_ptr,
            is_ref=ctype.is_ref,
            is_basic_type=ctype.is_basic_type,
        )

    # If a method has the keyword `This`, we replace it with the (instantiated) class.
    elif str_arg_type == 'This':
        # Check if the class is template instantiated
        # so we can replace it with the instantiated version.
        if instantiated_class:
            name = instantiated_class.original.name
            namespaces = instantiated_class.namespaces()
        else:
            name = cpp_type.name
            namespaces = cpp_type.namespaces

        return parser.Type(
            name=name,
            namespaces=namespaces,
            is_const=ctype.is_const,
            is_shared_ptr=ctype.is_shared_ptr,
            is_ptr=ctype.is_ptr,
            is_ref=ctype.is_ref,
            is_basic_type=ctype.is_basic_type,
        )

    # Case when 'This' is present in the type namespace, e.g `This::Subclass`.
    elif 'This' in str_arg_type:
        # Check if `This` is in the namespaces
        if 'This' in ctype.namespaces:
            # Simply get the index of `This` in the namespace and
            # replace it with the instantiated name.
            namespace_idx = ctype.namespaces.index('This')
            ctype.namespaces[namespace_idx] = cpp_type.name
        # Else check if it is in the template namespace, e.g vector<This::Value>
        else:
            for idx, template_param in enumerate(ctype.template_params):
                if 'This' in template_param.namespaces:
                    ctype.template_params[idx].namespaces = \
                        cpp_type.namespaces + [cpp_type.name]
        return ctype

    else:
        return ctype


def instantiate_args_list(args_list: Sequence[parser.Argument],
                          template_params: Sequence[parser.Type],
                          instantiations: Sequence[parser.Type],
                          cpp_type: parser.Type):
    """
    Instantiate template parameters in an argument list.
    Type with name `This` will be replaced by @p `cpp_type`.

    @param[in] args_list A list of `parser.Argument` to instantiate.
    @param[in] template_params List of template parameters to instantiate,
        e.g. ['T', 'U', 'V'].
    @param[in] instantiations List of specific types to instantiate, each
        associated with each template typename. Each type is a parser.Type,
        including its name and full namespaces.
    @param[in] cpp_type Full-namespace cpp class name of this instantiation
        to replace for arguments of type named `This`.
    @return A new list of parser.Argument which types are replaced with their
        instantiations.
    """
    instantiated_args = []
    for arg in args_list:
        new_type = instantiate_type(arg.type, template_params, instantiations,
                                    cpp_type)
        instantiated_args.append(
            parser.Argument(new_type, name=arg.name,
                            default=arg.default_value))
    return instantiated_args


def instantiate_return_type(return_type: parser.ReturnType,
                            template_params: Sequence[str],
                            instantiations: Sequence[parser.Type],
                            cpp_type: parser.Type,
                            instantiated_class: 'InstantiatedClass' = None):
    """Instantiate the return type."""
    new_type1 = instantiate_type(return_type.type1,
                                 template_params,
                                 instantiations,
                                 cpp_type,
                                 instantiated_class=instantiated_class)
    if return_type.type2:
        new_type2 = instantiate_type(return_type.type2,
                                     template_params,
                                     instantiations,
                                     cpp_type,
                                     instantiated_class=instantiated_class)
    else:
        new_type2 = ''
    return parser.ReturnType(new_type1, new_type2)


def instantiate_name(original_name: str,
                     instantiations: Sequence[parser.Type]):
    """
    Concatenate instantiated types with `original_name` to form a new
    instantiated name.

    NOTE: To avoid conflicts, we should include the instantiation's
    namespaces, but that is too verbose.
    """
    instantiated_names = []
    for inst in instantiations:
        # Ensure the first character of the type is capitalized
        name = inst.name
        # Using `capitalize` on the complete name causes other caps to be lower case
        instantiated_names.append(name.replace(name[0], name[0].capitalize()))

    return f"{original_name}{''.join(instantiated_names)}"


class InstantiationHelper:
    """
    Helper class for instantiation templates.
    Requires that `instantiation_type` defines a class method called
    `construct` to generate the appropriate object type.

    Signature for `construct` should be
    ```
        construct(method,
                  template_params,
                  class_instantiations,
                  method_instantiations,
                  instantiated_args,
                  parent=parent)
    ```
    """

    def __init__(self, instantiation_type: InstantiatedMember):
        self.instantiation_type = instantiation_type

    def instantiate(self, method: ClassMember, template_params: Sequence[str],
                    class_instantiations: Sequence[parser.Type],
                    method_instantiations: Sequence[parser.Type],
                    parent: 'InstantiatedClass') -> InstantiatedMember:
        """
        Instantiate both the class and method level templates.
        """
        instantiations = class_instantiations + method_instantiations

        instantiated_args = instantiate_args_list(method.args, template_params,
                                                  instantiations,
                                                  parent.cpp_type())

        return self.instantiation_type.construct(method,
                                                 template_params,
                                                 class_instantiations,
                                                 method_instantiations,
                                                 instantiated_args,
                                                 parent=parent)

    def multilevel_instantiation(
            self, methods_list: Sequence[ClassMember],
            template_params: Sequence[str],
            parent: 'InstantiatedClass') -> list[InstantiatedMember]:
        """
        Helper to instantiate methods at both the class and method level.

        Args:
            methods_list: The list of methods in the class to instantiated.
            template_params: List of class level template parameters, e.g. ['T'].
            parent: The instantiated class to which `methods_list` belongs.
        """
        instantiated_methods = []

        for method in methods_list:
            # We create a copy since we will modify the template_params list.
            method_template_params = deepcopy(template_params)

            if isinstance(method.template, parser.template.Template):
                method_template_params.extend(method.template.names)

                # Get all combinations of template args
                for instantiations in itertools.product(
                        *method.template.instantiations):

                    instantiated_methods.append(
                        self.instantiate(
                            method,
                            template_params=method_template_params,
                            class_instantiations=parent.instantiations,
                            method_instantiations=list(instantiations),
                            parent=parent))

            else:
                # If no method level templates, just use the class templates
                instantiated_methods.append(
                    self.instantiate(
                        method,
                        template_params=method_template_params,
                        class_instantiations=parent.instantiations,
                        method_instantiations=[],
                        parent=parent))

        return instantiated_methods
