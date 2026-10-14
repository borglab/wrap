#!/usr/bin/env python3
"""Generate a central Boost.Serialization library from interface declarations."""

import argparse
from pathlib import Path

from gtwrap.interface_parser import InterfaceParseError
from gtwrap.serialization_library import generate_library, write_library


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    parser.add_argument('--src', required=True, action='append', type=Path)
    parser.add_argument('--namespace-prefix', action='append', default=[])
    parser.add_argument('--ignore', action='append', default=[])
    parser.add_argument('--include', required=True, action='append')
    parser.add_argument('--out-dir', required=True, type=Path)
    args = parser.parse_args()
    try:
        sources = [(str(p), p.read_text(encoding='utf-8')) for p in args.src]
        files = generate_library(args.name, sources, args.include,
                                 args.namespace_prefix, args.ignore)
        write_library(args.out_dir, files)
    except (ValueError, OSError, InterfaceParseError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
