#! /usr/bin/env python
from __future__ import print_function

import sys

import json


def have_matching_versions(top_level_file, spec_file):
    """ first file should be the top level elm-package
        second file should be the spec file
    """

    with open(top_level_file) as f:
        top_level = json.loads(f.read())
        print(top_level_file, json.dumps(top_level, sort_keys=True, indent=4))

    with open(spec_file) as f:
        spec = json.loads(f.read())
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
        print('FAILED due to elm-deps mismatch, errors:')
        print('\n'.join(errors))
        return False
    else:
        print('Matching deps!')
        return True


if __name__ == '__main__':
    if len(sys.argv) > 2:
        top_level_file = sys.argv[1]
        spec_file = sys.argv[2]

        if not have_matching_versions(top_level_file, spec_file):
            sys.exit(1)

