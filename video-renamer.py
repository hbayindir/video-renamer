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
# 1: NOT IMPLEMENTED.

if __name__ == '__main__':
    
    # Set the logging level first:
    try:
        logging.basicConfig(filename = None, level = logging.DEBUG,
                            format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                            datefmt = '%Y-%m-%d %H:%M:%S')

        # Get the loca"l logger and start.
        localLogger = logging.getLogger('main')

        localLogger.debug('Logger setup completed.')
        localLogger.debug('%s is starting.', sys.argv[0])
    except IOError as exception:
        print ('Something about disk I/O went bad: ' + str(exception))
        sys.exit(1)

    # Let's start with building the argument parser.
    argumentParser = argparse.ArgumentParser()
    argumentParser.description = 'Rename many video files using their meta data with ease.'

    # Optional arguments are below.
    argumentParser.add_argument ('--alternative-exiftool', metavar = 'EXIFTOOL_PATH', help = 'Use an alternative exiftool binary, instead of the installed one.')
    argumentParser.add_argument ('-v', '--verbose', help = 'Print more detail about the process.', action = 'store_true')
    argumentParser.add_argument ('--fat32-safe', help = 'Rename files only with FAT32 safe characters.', action = 'store_true')
    argumentParser.add_argument ('--console-friendly', help = 'Do not use characters which need escaping in shells.', action = 'store_true')
    argumentParser.add_argument ('-V', '--version', help = 'Print ' + argumentParser.prog + ' version and exit.', action = 'version', version = argumentParser.prog + ' version 0.0.1')
    argumentParser.add_argument ('FILE', help = 'File to be renamed.', nargs = '+')

    arguments = argumentParser.parse_args()
