"""Pybind-specific annotations supported by wrapper interface files."""

from pyparsing import Regex

from .diagnostics import semantic_error
from .template import Template


PYBIND_ADAPTER = Regex(r"@pybind_adapter(?![A-Za-z0-9_])")


def _reject_annotation(source, location, tokens):
    """Raise a useful error for unknown or misplaced annotations."""
    annotation = tokens[0]
    if annotation == "@pybind_adapter":
        message = (
            "annotation '@pybind_adapter' can only be applied to a method, "
            "static method, or global function"
        )
    else:
        message = f"malformed or unknown annotation '{annotation}'"

    raise semantic_error(
        source,
        location,
        "callable annotation",
        message,
        "place '@pybind_adapter' after any template declaration and "
        "immediately before the callable declaration",
    )


UNSUPPORTED_ANNOTATION = Regex(r"@[^\s;{}()]+|@").set_parse_action(
    _reject_annotation)
UNSUPPORTED_TEMPLATED_ANNOTATION = (
    Template.rule.suppress() + UNSUPPORTED_ANNOTATION)
