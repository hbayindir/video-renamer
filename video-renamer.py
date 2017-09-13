#!/usr/bin/python3


# Video Renamer - A small tool to rename many video files at once using their meta data.
# Copyright (C) 2017  Hakan Bayindir
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging

import sys

if __name__ == '__main__':

    # Let's start with building the argument parser.
    argument_parser = argparse.ArgumentParser()
    argument_parser.description = 'Rename many video files using their meta data with ease.'

    # TODO: Add the options here.
    #       - Define external exiftool path.
    #       - Ability to define many files.
    arguments = argument_parser.parse_args()

    # Print the help if no arguments are given.
    if len(sys.argv) <= 1:
        argument_parser.print_help()
        sys.exit(1) # Exit with some code to show something went wrong.
