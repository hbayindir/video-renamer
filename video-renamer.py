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
    fileName = fileName.strip()
    
    # Let's change the '/' character. This is not valid neither in UNIX nor Windows
    fileName = fileName.replace('/', '_')
    
    # Replace the characters which need replace in FAT32. Got the tip from a tooltip (https://i.stack.imgur.com/2Jit2.png).
    if fat32Safe:
        for character in ['\\', ':', '*', '?', '"', '<', '>', '|']:
            fileName = fileName.replace(character, '_')
    
    # Replace characters which needs escaping. Got the list from holy stackoverflow (https://unix.stackexchange.com/q/270977/13922)
    if consoleFriendly:
        for character in ['`', '~', '!', '#', '$', '&', '*', '(', ')', '\t', '[', ']', '{', '}', '|', '\\', ';', '\'', '"', '<', '>', '?', ' ']:
            fileName = fileName.replace(character, '_')
    
    return fileName

'''
This function searches for a field name inside the metadata dictionary.
Since the ExifTool provides field names unprocessed(*), we need to look
for a field name that we want.

*: ExifTool provides the field names with its belonging class to find them easier (e.g.: QuickTime:Title, Composite:Rotation).
'''
def findField (metadata, fieldToFind):
    localLogger = logging.getLogger('findField')
    localLogger.debug('Will search for field %s', fieldToFind)
    
    foundFields = list ()
    
    # We need to search this stuff one by one.
    # A loop, and text processing. A recipe for low performance code.
    for field in metadata:
        processedField = field.strip().split(':')
        localLogger.debug('Field %s is processed as %s.', field, processedField)
        
        for processedFieldElement in processedField:
            if str(processedFieldElement) == fieldToFind:
                localLogger.debug('Field %s contains the field name we are searching for, adding to results.', field)
                foundFields.append(metadata[field])
        
    
    localLogger.debug('Found %s field(s) in metadata, returning results.', str(len(foundFields)))
    return foundFields

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
    argumentParser.add_argument ('--dry-run', help = 'Do not actually rename files, print actions to be taken (implies -vv).', action = 'store_true')
    argumentParser.add_argument ('-v', '--verbose', help = 'Print more detail about the process. Using more than one -v increases verbosity.', action = 'count')
    argumentParser.add_argument ('-q', '--quiet', help = 'Do not print anything to console (overrides verbose).', action = 'store_true') # Will override --verbose.

    # Ability to handle version in-library is nice.
    argumentParser.add_argument ('-V', '--version', help = 'Print ' + argumentParser.prog + ' version and exit.', action = 'version', version = argumentParser.prog + ' version 0.0.2')

    # Mandatory FILE(s) argument. nargs = '+' means "at least one, but can provide more if you wish"
    argumentParser.add_argument ('FILE', help = 'File(s) to be renamed.', nargs = '+')

    arguments = argumentParser.parse_args()

    if arguments.verbose == None:
        arguments.verbose = 0;

    # Elevate logging level if dry run is enabled.
    if arguments.dry_run == True and arguments.verbose < 2:
        arguments.verbose = 1;

    # At this point we have the required arguments, let's start with logging duties.
    if arguments.verbose != None :
        if arguments.verbose == 1:
            LOGGING_LEVEL = logging.INFO
        elif arguments.verbose == 2:
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
                # Need to search for a title field here. Let's take a look.
                requestedField = findField(metadata, 'Title')
                                                
                # We may have metadata collision, warn people.                                                
                if len(requestedField) > 1:
                    localLogger.warning ('There a more than one field which contains the title. Please make sure the file is renamed correctly.')
                
                if len(requestedField) == 0:
                    localLogger.error ('No matching fields found for file %s, will skip.', metadata['File:FileName'])
                    continue
                                
                # Get the normalized file name and add the extension. Make extension lower case to make things look better.
                normalizedFileName = normalizeFileName(requestedField[0], fat32Safe = arguments.fat32_safe, consoleFriendly = arguments.console_friendly) + '.' + metadata['File:FileTypeExtension'].lower()
                
                # Talk to me!
                localLogger.info('Will rename file %s to %s.', metadata['File:FileName'], normalizedFileName )
                         
                if arguments.dry_run == False:
                    os.rename(metadata['File:Directory'] + '/' + metadata['File:FileName'], metadata['File:Directory'] + '/' + normalizedFileName)
                
    except FileNotFoundError as exception:
        localLogger.error (exception)
        sys.exit (3)