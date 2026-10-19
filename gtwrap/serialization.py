"""Discover and generate centrally owned Boost.Serialization support."""

from dataclasses import dataclass
import re

from gtwrap import interface_parser as parser
from gtwrap import template_instantiator as instantiator


def export_name(cpp_type):
    """Preserve the identifiers historically emitted by the Python wrapper."""
    return re.sub('[,:<> ]', '', cpp_type) if ',' in cpp_type else cpp_type


def is_serializable(cls):
    """Use the same instantiated method markers as ordinary Python wrapping."""
    return any(method.to_cpp() in ('serialize', 'serializable')
               for method in list(cls.methods) + list(cls.static_methods))


@dataclass(frozen=True)
class Export:
    cpp_type: str
    name: str
    source: str


def discover(sources, namespace_prefixes=(), ignore_classes=()):
    """Collect exports from ``(source name, interface text)`` pairs in order.

    Selection happens after template instantiation, so aliases and explicit
    instantiations have exactly the names used by the ordinary wrapper.
    """
    for prefix in namespace_prefixes:
        if not prefix or not prefix.endswith('::'):
            raise ValueError('namespace prefixes must be nonempty and end in ::')
    ignored = set(ignore_classes)
    exports = {}
    names = {}

    def visit(namespace, source):
        for element in namespace.content:
            if isinstance(element, parser.Namespace):
                visit(element, source)
            elif isinstance(element, instantiator.InstantiatedClass):
                cpp_type = element.to_cpp()
                if (cpp_type in ignored or not is_serializable(element)
                        or (namespace_prefixes and not any(
                            cpp_type.startswith(p) for p in namespace_prefixes))):
                    continue
                name = export_name(cpp_type)
                if name in names and names[name].cpp_type != cpp_type:
                    previous = names[name]
                    raise ValueError(
                        f'{source}: export identifier {name!r} for {cpp_type} '
                        f'conflicts with {previous.cpp_type} in {previous.source}')
                entry = Export(cpp_type, name, source)
                exports.setdefault(cpp_type, entry)
                names.setdefault(name, entry)

    source_names = []
    for source, content in sources:
        source_names.append(source)
        module = parser.Module.parse_string(content, source_name=source)
        visit(instantiator.instantiate_namespace(module), source)
    if not exports:
        raise ValueError(f'{", ".join(source_names)}: no serializable types matched')
    return list(exports.values())
