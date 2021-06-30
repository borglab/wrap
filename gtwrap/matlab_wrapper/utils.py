"""Mixins for reducing the amount of boilerplate in the main wrapper class."""

class CheckMixin:
    """Mixin to provide various checks."""
    # Data types that are primitive types
    not_ptr_type = ['int', 'double', 'bool', 'char', 'unsigned char', 'size_t']
    # Ignore the namespace for these datatypes
    ignore_namespace = ['Matrix', 'Vector', 'Point2', 'Point3']
    # Methods that should be ignored
    ignore_methods = ['pickle']
    # Methods that should not be wrapped directly
    whitelist = ['serializable', 'serialize']
    # Datatypes that do not need to be checked in methods
    not_check_type: list = []

    def _has_serialization(self, cls):
        for m in cls.methods:
            if m.name in self.whitelist:
                return True
        return False

    def is_shared_ptr(self, arg_type):
        """
        Determine if the `interface_parser.Type` should be treated as a
        shared pointer in the wrapper.
        """
        return arg_type.is_shared_ptr or (
            arg_type.typename.name not in self.not_ptr_type
            and arg_type.typename.name not in self.ignore_namespace
            and arg_type.typename.name != 'string')

    def is_ptr(self, arg_type):
        """
        Determine if the `interface_parser.Type` should be treated as a
        raw pointer in the wrapper.
        """
        return arg_type.is_ptr or (
            arg_type.typename.name not in self.not_ptr_type
            and arg_type.typename.name not in self.ignore_namespace
            and arg_type.typename.name != 'string')

    def is_ref(self, arg_type):
        """
        Determine if the `interface_parser.Type` should be treated as a
        reference in the wrapper.
        """
        return arg_type.typename.name not in self.ignore_namespace and \
               arg_type.typename.name not in self.not_ptr_type and \
               arg_type.is_ref
