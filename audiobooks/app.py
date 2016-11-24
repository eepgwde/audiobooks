#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create an audiobook from files given as input or from a file and output to file.

Usage:
  audiobooks (-h | --help)
  audiobooks [-o FILE] [-f FILE]... [options] [<input>]...

Arguments:
  input                                 Files, directories, or glob patterns to include.

Options:
  -h, --help                            Display help message.
  -l, --log                             Enable gmusicapi logging.
  -d, --dry-run                         Output options and files
  -q, --quiet                           Don't output status messages.
  -v, --verbose                         Output status messages.
                                        With -l,--log will display warnings.
                                        With -d,--dry-run will show parameters.
  -o FILE, --output FILE                Output filename to write to.
  -f FILE, --files FILE                 File containing files.
  --cover FILE                          Add a file of cover-art
  -c COMMAND, --command COMMAND         What to do: chapters

Patterns can be any valid Python regex patterns.
"""

from __future__ import print_function;

from audiobooks._Track import Track

from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4Cover, MP4
from mutagen.mp4 import AtomDataType
from mutagen.easymp4 import EasyMP4

from unidecode import unidecode
from docopt import docopt

import csv
import os
import sys
import glob
import subprocess

from math import floor
from operator import attrgetter
from tempfile import mkstemp

import logging

QUIET = 25
logging.addLevelName(25, "QUIET")

logging.basicConfig(filename='audiobooks.log', level=QUIET)
logger = logging.getLogger('Test')

CHAPTER_TEMPLATE = """CHAPTER%(CHAPNUM)s=%(HOURS)02d:%(MINS)02d:%(SECS)02d
CHAPTER%(CHAPNUM)sNAME=%(CHAPNAME)s
"""
MERGE_COMMAND = "MP4Box"
CHAPS_COMMAND = "mp4chaps"

cli = None

def get_tracks(dir_name='.'):
    """get track titles and lengths

    track file extensions *must* end with .m4a"""
    track_files = glob.glob(os.path.join(dir_name, '*.m4a'))
    track_list = [Track(track_file) for track_file in track_files]
    track_list = sorted(track_list, key=attrgetter('disc_track'))
    return track_list

def write_csv(output_fname, tracks):
    """write csv file with track numbers and title

    writes to output_fname, expects track list as input"""
    with open(output_fname, 'w') as csv_file:
        track_writer = csv.writer(csv_file)
        for track in tracks:
            track_writer.writerow(
                [track.disc_track[0], track.disc_track[1],
                 track.fname,
                 track.title.encode('utf-8'),
                 track.duration,
                 ]
            )

def write_chaplist(output_fname, tracks):
    """write MP4Box compatible chapter marks file

    writes to output_fname, expects track list as input"""
    output_lines = []
    for track_number, track in enumerate(tracks):
        mins, secs = divmod(track.duration, 60)
        hours, mins = divmod(mins, 60)
        output_lines.append(
            CHAPTER_TEMPLATE % {'CHAPNUM':track_number,
                                 'HOURS':hours, 'MINS':mins, 'SECS':secs,
                                 'CHAPNAME':track.title.encode('utf-8')
                               }
        )
    with open(output_fname, 'w') as output_file:
        output_file.writelines(output_lines)
    return output_fname

def combine_files(output_fname, tracks, chaplist_fname):
    """combine m4a files to one big file

    writes to output_fname, expects track list as input"""
    merge_cmd_and_args = []
    for track in tracks:
        merge_cmd_and_args.append('-cat')
        merge_cmd_and_args.append(track.fname)
    merge_cmd_and_args.insert(0, MERGE_COMMAND)
    merge_cmd_and_args.extend(['-chap', chaplist_fname])
    merge_cmd_and_args.append(output_fname)
    merge_call = subprocess.call(merge_cmd_and_args)
    if merge_call != 0:
        raise RuntimeError('Merge unsuccessful')
    if subprocess.call(
        [CHAPS_COMMAND, '--convert', '--chapter-qt', output_fname]
    ) != 0:
        raise RuntimeError('Could not convert to QT chapter marks')
    return output_fname

def write_audio_metadata(output_fname, album, artist):
    """Write album and artist information to audiobook file

    changes output_fname on the fly, expects album and artist"""
    track = EasyMP4(output_fname)
    track['album'] = album
    track['title'] = album
    track['artist'] = artist
    track.save()

def write_audio_cover(output_fname, cover_fname):
    """Write cover image to audiobook file

    changes output_fname on the fly, expects cover_fname"""
    if cover_fname.endswith('png'):
        picture_type = AtomDataType.PNG
    else:
        picture_type = AtomDataType.JPEG
    with open(cover_fname, 'rb') as album_art_file:
        album_art = MP4Cover(
                        data=album_art_file.read(),
                        imageformat=picture_type
                    )
    track = MP4(output_fname)
    track['covr'] = [album_art]
    track.save()

def cli_run(argv):
    global cli
    cli = dict((key.lstrip("-<").rstrip(">"), value) for key, value in docopt(__doc__).items())

    enable_logging = cli['log']
    if cli['quiet']:
        logger.setLevel(QUIET)
    else:
        logger.setLevel(logging.INFO)

    if enable_logging:
        logger.setLevel(logging.DEBUG)
        if cli['verbose']:
            sh = logging.StreamHandler()
            logger.addHandler(sh)

    for k in cli.items():
        logger.info(k)

    if len(cli['input']) > 0:
        tracks = get_tracks(os.path.abspath(cli['input'][0]))
    elif len(cli['files']) > 0:
        tracks = get_tracks(os.path.abspath(cli['files'][0]))
    else:
        return

    if cli['dry-run']:
        logger.info('tracks: ' + str(len(tracks)))
        return
    
    if cli['output']:
        output_fname = cli['output']
    else:
        output_fname = "%s.m4b" % os.path.join(
            cli['output'],
            tracks[0].album.encode('utf-8')
        )

    if cli['cover']:
        cover_fname = cli['cover']
    else:
        cover_fname = os.path.join(cli['output'], 'cover.jpg')


    chapter_fname = mkstemp(prefix='chaplist')[1]
    try:
        logger.info("gathering chapter information")
        write_chaplist(chapter_fname, tracks)
    except:
        raise

    try:
        logger.info("combining audio tracks")
        combine_files(output_fname, tracks, chapter_fname)
    except:
        raise
    
    try:
        logger.info("writing original metadata to new audiobook")
        write_audio_metadata(output_fname,
                             album=tracks[0].album,
                             artist=tracks[0].artist,
        )
    except:
        raise

    try:
        logger.info("adding cover image if available")
        write_audio_cover(output_fname, cover_fname)
    except IOError:
        logger.info("unable to add cover image.")
    

def main():
    """entrypoint without arguments"""
    raise SystemExit(cli_run(sys.argv))

if __name__ == '__main__':
    main()
