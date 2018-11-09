#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import splitext, join, getmtime, isdir, basename, exists, abspath
from os import walk, makedirs
from argparse import ArgumentParser
from shutil import copy
from time import gmtime, strftime
from pyexiv2 import ImageMetadata


import logging
log = logging.getLogger(__name__)

LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'


def index(source, destination_dir):
    """
    @param source Source filename to copy.
    @param destinationDir Destination base directory to copy source to. Final
    directory name is determined from file.
    """
    try:
        # Load EXIF information
        metadata = ImageMetadata(source)
        metadata.read()
        # Read the date/time at which the picture was taken
        tag = metadata['Exif.Image.DateTime']
        mtime = tag.value.timetuple()
        log.debug('Successfully read EXIF from "{s}"'.format(s=source))
    except Exception as e:
        log.debug(e)
        # Get the last modification time
        mtime = gmtime(getmtime(source))

    # Destination filename
    destination = join(destination_dir, strftime('%Y', mtime),
                       strftime('%Y-%m-%d', mtime))
    # Directory must exist
    if not isdir(destination):
        log.debug(f'Create directory: "{destination}"')
        makedirs(destination, 0o755)
    # Append filename from source
    destination = join(destination, basename(source))
    log.debug(f'Destination: "{destination}"')

    # Check if file already exists, skip if it does
    if exists(destination):
        log.info('Skipping "{d}", file already exists'.format(d=destination))
        return
    log.info('Copying file "{s}" to directory "{d}"'.format(s=source,
                                                            d=destination))
    # Copy file
    copy(source, destination)


def logger(options):
    """ """
    # Set up logging
    if options.log:
        handler = logging.FileHandler(options.log)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%H:%M:%S'))
    # Add handler to the root log
    logging.root.addHandler(handler)
    # Set log level
    level = logging.DEBUG if options.debug else logging.INFO
    logging.root.setLevel(level)


def parse():
    """ TODO: Docstring for parse. """
    parser = ArgumentParser()
    # Shared
    parser.add_argument('--debug', help='enable debug mode',
                        action="store_true", default=False)
    parser.add_argument('--log', help='log file')
    parser.add_argument('--input-dir', type=abspath, required=True,
                        help='input directory')
    parser.add_argument('--output-dir', type=abspath, required=True,
                        help='input directory')
    parser.add_argument('--extension', action='append', required=True,
                        help='extensions')
    # Parse options
    return parser.parse_args()


def main():
    """Main entry point
    :returns: TODO
    """
    options = parse()
    try:
        # Setup logging
        logger(options)

        # Find all files in directory recursively
        for root, directories, filenames in walk(options.input_dir):
            # Process only the provided extensions
            for filename in filter(lambda x: splitext(x)[1] in
                                   options.extension, filenames):
                try:
                    index(join(root, filename), options.output_dir)
                except Exception as e:
                    # Log the exception but keep going
                    log.error(e)

        # Success
        return(0)
    except KeyboardInterrupt:
        log.info('Received <ctrl-c>, stopping')
    except Exception as e:
        log.exception(e) if options.debug else log.error(e)
    finally:
        # Return 1 on any caught exception
        return(1)


if __name__ == '__main__':
    exit(main())
