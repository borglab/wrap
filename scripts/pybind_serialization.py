#!/usr/bin/env python3
"""Generate shared Boost export keys from a pybind interface.

The implementation fragment is for an extension that does not already own
full BOOST_CLASS_EXPORT registrations for these types. It must be included
once, after that extension's archive headers and the generated key header.
"""

import argparse
from pathlib import Path

from gtwrap.pybind_wrapper import PybindWrapper


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--src', required=True, type=Path)
    parser.add_argument('--namespace-prefix', required=True)
    parser.add_argument('--include', action='append', default=[],
                        help='C++ header defining the selected types; repeatable')
    parser.add_argument('--out-header', required=True, type=Path)
    parser.add_argument('--out-implementations', required=True, type=Path)
    args = parser.parse_args()

    wrapper = PybindWrapper(module_name='', top_module_namespaces=[''],
                            use_boost_serialization=True)
    keys, implementations = wrapper.serialization_support(
        args.src.read_text(encoding='utf-8'), args.namespace_prefix,
        args.include)
    if not implementations.strip():
        parser.error('no serializable types matched --namespace-prefix')
    args.out_header.parent.mkdir(parents=True, exist_ok=True)
    args.out_implementations.parent.mkdir(parents=True, exist_ok=True)
    args.out_header.write_text(keys, encoding='utf-8')
    args.out_implementations.write_text(implementations, encoding='utf-8')


if __name__ == '__main__':
    main()
