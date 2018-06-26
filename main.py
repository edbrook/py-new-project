#!/usr/bin/env python3

import argparse
import sys
from py_project import PyProject


def parse_args():
    parser = argparse.ArgumentParser(description="Setup a new Python project")

    parser.add_argument('-m', '--module', action='store_true',
        default=False, help="The new project is a Python module")
    
    git_group = parser.add_mutually_exclusive_group()
    git_group.add_argument('-g', '--git', action='store_false',
        default=True, help="Suppress initialisation of git repository")
    git_group.add_argument('-gh', '--git-hub', action='store_true',
        default=False, help="Create an initial commit and push to GitHub.")

    parser.add_argument('name', type=str, nargs=1,
        help="The new project's name")

    args = parser.parse_args()

    # Git is implied if the GitHub option has been selected
    if args.git_hub == True:
        args.git = True
    
    return args


if __name__ == '__main__':
    args = vars(parse_args())
    args['name'] = args['name'][0]
    try:
        project = PyProject(**args)
        project.create()
    except FileExistsError:
        sys.stderr.write('"{}" already exists!\n'.format(args['name']))