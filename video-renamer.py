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

# List of exit codes:
# 0: Everything went as planned.
# 1: Help is printed.
# 2: Version is printed.

if __name__ == '__main__':

    # Let's start with building the argument parser.
    argumentParser = argparse.ArgumentParser()
    argumentParser.description = 'Rename many video files using their meta data with ease.'

    # Optional arguments are below.
    argumentParser.add_argument ('--alternative-exiftool', help = 'Use an alternative exiftool binary, instead of the installed one.')
    argumentParser.add_argument ('-v', '--verbose', help = 'Print more detail about the process.', action = 'store_true')
    argumentParser.add_argument ('-V', '--version', help = 'Print ' + argumentParser.prog + ' version and exit.', action = 'store_true')

    # TODO: Add the options here.
    #       - Ability to define many files.
    arguments = argumentParser.parse_args()

    # Print the help if no arguments are given.
    if len(sys.argv) <= 1:
        argumentParser.print_help()
        sys.exit (1) # Exit with some code to show something went wrong.

    if arguments.version:
        print (argumentParser.prog + ' version 0.0.1')
        sys.exit (2) # Exit with a distinct error code to indicate what happened.
