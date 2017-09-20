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

# Import core packages first.
import sys

# Then utilities.
import argparse
import logging

# External packages come last.
import exiftool

# List of exit codes:
# 0: Everything went as planned.
# 1: Cannot initialize logging subsystem.
# 2: Exiftool is not found.

# TODO: Implement quiet switch.


if __name__ == '__main__':

    # This is the global logging level. Will be changed with verbosity if required in the future.
    LOGGING_LEVEL = logging.ERROR

    # Let's start with building the argument parser.
    argumentParser = argparse.ArgumentParser()
    argumentParser.description = 'Rename many video files using their meta data with ease.'

    # Optional arguments are below.
    argumentParser.add_argument ('--alternative-exiftool', metavar = 'EXIFTOOL_PATH', help = 'Use an alternative exiftool binary, instead of the installed one.')
    # Count gives the number of '-v' s provided. So one can handle the verbosity easily.
    argumentParser.add_argument ('-v', '--verbose', help = 'Print more detail about the process.', action = 'count')
    argumentParser.add_argument ('-q', '--quiet', help = 'Do not print anything to console.', action = 'store_true') # Will override --verbose.
    argumentParser.add_argument ('--fat32-safe', help = 'Rename files only with FAT32 safe characters.', action = 'store_true')
    argumentParser.add_argument ('--console-friendly', help = 'Do not use characters which need escaping in shells.', action = 'store_true')

    # Ability to handle version in-library is nice.
    argumentParser.add_argument ('-V', '--version', help = 'Print ' + argumentParser.prog + ' version and exit.', action = 'version', version = argumentParser.prog + ' version 0.0.1')

    # Mandatory FILE(s) argument. nargs = '+' means "at least one, but can provide more if you wish"
    argumentParser.add_argument ('FILE', help = 'File(s) to be renamed.', nargs = '+')

    arguments = argumentParser.parse_args()

    # At this point we have the required arguments, let's start with logging duties.
    if arguments.verbose != None :
        if arguments.verbose == 1:
            LOGGING_LEVEL = logging.WARN
        elif arguments.verbose == 2:
            LOGGING_LEVEL = logging.INFO
        elif arguments.verbose >= 3:
            LOGGING_LEVEL = logging.DEBUG

    # Set the logging level first:
    try:
        logging.basicConfig(filename = None, level = LOGGING_LEVEL,
                            format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                            datefmt = '%Y-%m-%d %H:%M:%S')

        # Get the loca"l logger and start.
        localLogger = logging.getLogger('main')

        localLogger.debug('Logger setup completed.')
        localLogger.debug('%s is starting.', sys.argv[0])
    except IOError as exception:
        print ('Something about disk I/O went bad: ' + str(exception))
        sys.exit(1)
    
    # If the logger is up, we can start building the PyExifTool wrapper.
    try:
        with exiftool.ExifTool(executable_ = arguments.alternative_exiftool) as et:
            metadata = et.get_metadata_batch(files)
    except FileNotFoundError as exception:
        localLogger.error('Exiftool binary is not found, exiting.')
        sys.exit (2)