#! /usr/bin/env python
from __future__ import print_function

import sys
import json
import requests
import struct

def load_all_packages(elm_version):
    payload = requests.get("http://package.elm-lang.org/all-packages?elm-package-version={elm_version}".format(
        elm_version=elm_version
        ))

    return { item['name'] : item for item in payload.json() }

def load_versions(package_name):
    payload = requests.get("http://package.elm-lang.org/versions?name={package_name}".format(
        package_name=package_name
        ))

    return payload.content


def load_local_packages(elm_package):
    with open(elm_package) as f:
        return json.load(f)

def top_range(field):
    only_end = field[field.index('v'):]

    if '=' in only_end:
        return only_end.split('=')[-1].strip()
    if '<' in only_end:
        return only_end.split('<')[-1].strip()

def major(version):
    return int(version.split('.')[0])

def minor(version):
    return int(version.split('.')[1])

def patch(version):
    return int(version.split('.')[2])

def get_major_upgrades(top, versions):
    major_top = major(top)

    return [ version for version in versions if major(version) > major_top ]

def get_minor_upgrades(top, versions):
    major_top = major(top)
    minor_top = minor(top)

    return [ version for version in versions if minor(version) > minor_top and major(version) == major_top ]

def get_patch_upgrades(top, versions):
    major_top = major(top)
    minor_top = minor(top)
    patch_top = patch(top)

    return [ version for version in versions
        if major(version) == major_top and minor_top == minor(version) and patch_top > patch(version) ]

def print_newer_versions(local_deps, remote_deps):

    upgrade_suggestions = []

    for (dep, version) in local_deps.items():
        current_version = top_range(version)
        patches = get_patch_upgrades(current_version, remote_deps[dep]['versions'])
        minors = get_minor_upgrades(current_version, remote_deps[dep]['versions'])
        majors = get_major_upgrades(current_version, remote_deps[dep]['versions'])

        if len(patches) > 0:
            upgrade_suggestions.append(
                'Patches available for {dep}: [{patches}]'.format(dep=dep, patches=', '.join(patches))
                )
        if len(minors) > 0:
            upgrade_suggestions.append(
                'Minors available for {dep}: [{minors}]'.format(dep=dep, minors=', '.join(minors))
                )
        if len(majors) > 0:
            upgrade_suggestions.append(
                'Majors available for {dep}: [{majors}]'.format(dep=dep, majors=', '.join(majors))
                )

    if not upgrade_suggestions:
        print('No upgrades avaible')
    else:
        print('\n'.join(upgrade_suggestions))



if __name__ == '__main__':

    if len(sys.argv) > 1:
        local = load_local_packages(sys.argv[1])
        remote = load_all_packages('0.16')
        print_newer_versions(local['dependencies'], remote)

