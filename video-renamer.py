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
import os
import sys

# Then utilities.
import argparse
import logging
import glob

# External packages come last.
import exiftool

# List of exit codes:
# 0: Everything went as planned.
# 1: Cannot initialize logging subsystem.
# 2: No files to rename.
# 3: Exiftool is not found.

'''
normalizeFileName: Check the filename string and modify the string if required.

This function will make sure that the file names are UNIX safe, and will support more
restrictive modes.

- UNIX compatibility will assume that only '/' and NULL is invalid.
- FAT32 Safe: Will only use FAT32 safe characters.
- Console Friendly: Will only use characters which doesn't need escaping in UNIX shells.

This function will change all restricted characters and console-unfriendly characters with '_'.
'''
def normalizeFileName (fileName, fat32Safe = False, consoleFriendly = False):
    # Get the lgger and print some debug information.
    localLogger = logging.getLogger ('normalizeFileName')
    localLogger.debug('File name to normalize is "%s"', fileName)
    localLogger.debug('FAT32 safety is set to %s', fat32Safe)
    localLogger.debug('Console friendly renaming is set to %s', consoleFriendly)
    
    # Standard file treatments
    normalizedFileName = fileName.strip()
    
    # Let's change the '/' character.
    normalizedFileName = fileName.replace('/', '_')
    
    return normalizedFileName

if __name__ == '__main__':
    # This is the global logging level. Will be changed with verbosity if required in the future.
    LOGGING_LEVEL = logging.ERROR

    # Let's start with building the argument parser.
    argumentParser = argparse.ArgumentParser()
    argumentParser.description = 'Rename many video files using their meta data with ease.'
    argumentParser.epilog = 'In order to match recursive files correctly, please put your wildcard containing paths into single quotes.'

    # Optional arguments are below.
    argumentParser.add_argument ('--alternative-exiftool', metavar = 'EXIFTOOL_PATH', help = 'Use an alternative exiftool binary, instead of the installed one.')
    # Count gives the number of '-v' s provided. So one can handle the verbosity easily.
    argumentParser.add_argument ('--fat32-safe', help = 'Rename files only with FAT32 safe characters.', action = 'store_true')
    argumentParser.add_argument ('--console-friendly', help = 'Do not use characters which need escaping in shells.', action = 'store_true')
    argumentParser.add_argument ('-r', '--recursive', help = 'Work recursively on the given path.', action = 'store_true')
    argumentParser.add_argument ('-v', '--verbose', help = 'Print more detail about the process. Using more than one -v increases verbosity.', action = 'count')
    argumentParser.add_argument ('-q', '--quiet', help = 'Do not print anything to console (overrides verbose).', action = 'store_true') # Will override --verbose.

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
        logging.basicConfig(filename = None, level = LOGGING_LEVEL, format = '%(levelname)s: %(message)s')

        # Get the loca"l logger and start.
        localLogger = logging.getLogger('main')

        # Disable logging if quiet switch is set.
        if arguments.quiet == True:
            logging.disable(logging.CRITICAL) # Critical is the highest built-in level. This line disables CRITICAL and below.

        localLogger.debug('Logger setup completed.')
        localLogger.debug('%s is starting.', sys.argv[0])
    except IOError as exception:
        print ('Something about disk I/O went bad: ' + str(exception), file = sys.stderr)
        sys.exit(1)

    # Need to expand the files with glob first.
    filesToWorkOn = list ()

    # Let's print some information about the passed parameters.
    localLogger.debug('Recursiveness is set to %s.', arguments.recursive)
    localLogger.debug('FAT32 safety is set to %s.', arguments.fat32_safe)
    localLogger.debug('Console friendliness is set to %s.', arguments.console_friendly)

    # Let's get the passed files from arguments, and work on them.
    localLogger.debug ('Files to be processed are: %s.', arguments.FILE)

    # File path handling is not easy. We need to expand the vars, the user and glob it to see how many files we get.
    # Oh, don't forget the recursive switch too.
    for inputFile in arguments.FILE:
        possibleFiles = glob.iglob (os.path.expanduser (os.path.expandvars (inputFile)), recursive = arguments.recursive)

        # Not all returned glob paths are existing files. We need to verify each one.
        # The loop is here, because glob expands regex to independent files.
        for possibleFile in possibleFiles:
            if os.path.isfile (possibleFile):
                filesToWorkOn.append(possibleFile)

    # This is the final list we work on. It may be empty or, well... long.
    localLogger.debug ('Final file list is: %s', filesToWorkOn)
    localLogger.info ('Matched %d files to rename.', len(filesToWorkOn))


    if len(filesToWorkOn) == 0:
        localLogger.error ('No files match againts the given FILE arguments, aborting.')
        sys.exit (2)
        
    # If the logger is up, we can start building the PyExifTool wrapper.
    try:
        with exiftool.ExifTool(executable_ = arguments.alternative_exiftool) as et:
            fileMetadata = et.get_metadata_batch(filesToWorkOn)

            for metadata in fileMetadata:
                # localLogger.info ("Title of the file " + metadata["SourceFile"] + ": " +  metadata["QuickTime:Title"])
                pass
    except FileNotFoundError as exception:
        localLogger.error ('Exiftool binary is not found, exiting.')
        sys.exit (3)
