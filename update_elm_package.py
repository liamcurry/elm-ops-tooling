#! /usr/bin/env python
from __future__ import print_function

import elm_deps_upgrade as upgrader
from collections import OrderedDict
import json
import requests
import argparse
import sys

KNOWN_MOVES = {
    'evancz/elm-html' : 'elm-lang/html'
    , 'evancz/virtual-dom': 'elm-lang/virtual-dom'
    , 'evancz/elm-effects' : ''
    , 'evancz/start-app' : ''
    , 'maxsnew/lazy' : 'elm-lang/lazy'
    }


def upgrade_elm_version(version):
    return "0.17.0 <= v < 0.18.0"

def new_packages():
    r = requests.get("http://159.203.88.24:8000/new-packages")
    return r.json()

def update_elm_package(root_folder, dry=False):
    with open(root_folder + '/elm-package.json') as f:
        package_data = json.load(f, object_pairs_hook=OrderedDict)

    package_data['elm-version'] = upgrade_elm_version(package_data['elm-version'])

    packages = package_data['dependencies']
    upgraded_packages = new_packages()

    notes = []
    errors = []
    upgradable_packages = {}

    for (package, version) in packages.items():
        if package in KNOWN_MOVES:
            new_name = KNOWN_MOVES[package]

            if new_name == '':
                errors.append('Package {name} has been removed'.format(name=package))
            else:
                notes.append('Package {name} renamed to {new_name}'.format(name=package, new_name=new_name))
                package = new_name
                version = '1.0.0 <= v <= 1.0.0'
                upgradable_packages[package] = version

            continue

        if package not in upgraded_packages:
            errors.append('Package {name} not upgraded yet!'.format(name=package))
            continue


        upgradable_packages[package] = version

    local = upgradable_packages
    remote = upgrader.load_all_packages("0.17", "http://159.203.88.24:8000/all-packages?elm-package-version=")


    upgrade_suggestions = upgrader.find_newer_versions(local, remote)

    for (dep, suggestions) in upgrade_suggestions.items():
        try:
            update_to = upgrader.newest_version(suggestions)
        except Exception as e:
            notes.append('package {} already updated'.format(dep))
            continue

        notes.append('updating {} to {}'.format(dep, update_to))

        package_data['dependencies'][dep] = "{} <= v <= {}".format(update_to, update_to)


    print('=======================')
    print('Notes:')
    print('\n'.join(notes))

    print('=======================')
    print('Warnings: ')
    print('\n'.join(errors))

    print('========================\n\n')
    print(json.dumps(package_data, sort_keys=False, indent=4))

    if not dry:
        with open(root_folder + '/elm-package.json', 'w') as f:
            json.dump(package_data, f, sort_keys=False, indent=4)

    if errors:
        print('There were errors that need to be handled manually!')
        sys.exit(1)




def main():

    parser = argparse.ArgumentParser(description='Automatically upgrade your package to 0.17')
    parser.add_argument('--dry', '-d', action='store_true', help='only print possible changes', default=False)

    parser.add_argument('package_dir')
    args = parser.parse_args()

    update_elm_package(args.package_dir, dry=args.dry)


if __name__ == '__main__':
    main()

