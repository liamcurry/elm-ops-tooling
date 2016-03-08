#! /usr/bin/env python
from __future__ import print_function

import sys
import json
import argparse


def have_matching_versions(top_level_file, spec_file, is_exact=False, quiet=True):
    """ first file should be the top level elm-package exact-dependencies.json
        second file should be the spec file
    """

    with open(top_level_file) as f:
        top_level = json.load(f)

    with open(spec_file) as f:
        spec = json.load(f)

    if not is_exact:
        top_level = top_level['dependencies']
        spec = spec['dependencies']

    if not quiet:
        print(top_level_file, json.dumps(top_level, sort_keys=True, indent=4))
        print(spec_file, json.dumps(spec, sort_keys=True, indent=4))

    errors = []

    for (package_name, package_version) in top_level.items():
        if package_name not in spec:
            errors.append('Package {package_name} not found in {spec_file}, but was found in {top_level_file}'.format(
                package_name=package_name, spec_file=spec_file, top_level_file=top_level_file)
            )
        elif spec[package_name] != package_version:
            errors.append('Package version mismatch for'
                ' {package_name}!\n\n {top_level_file} had {package_version}\n {spec_file} had {other_package_version}'.format(
                    package_version=package_version, package_name=package_name, top_level_file=top_level_file,
                    spec_file=spec_file, other_package_version=spec[package_name])
                )

    if len(errors) > 0:
        print('BUILD FAILED due to elm-deps mismatch, errors:')
        print('\n'.join(errors))
        return False
    else:
        print('Matching deps!')
        return True

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--quiet', '-q', action='store_true', help='don\'t print anything')
    parser.add_argument('--exact', '-e', action='store_true', help='these files are exact dependencies')

    parser.add_argument('top_level_file')
    parser.add_argument('spec_file')
    args = parser.parse_args()

    if not have_matching_versions(args.top_level_file, args.spec_file, quiet=args.quiet, is_exact=args.exact):
        sys.exit(1)


if __name__ == '__main__':
    main()
