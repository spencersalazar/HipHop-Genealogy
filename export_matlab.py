#!/usr/bin/python

import sys
import os
import json
import uuid
import mutagen

### Load data ###

META_FILE = 'meta.json'
GENRES_LIST_FILE = 'genres.json'
ARTISTS_LIST_FILE = 'artists.json'
WAV_DIR = 'wav'

FILENAMES_DATFILE = 'files.dat'
METADATA_DATFILE = 'meta.dat'

if len(sys.argv) >= 1:
    FILENAMES_DATFILE = sys.argv[1]
if len(sys.argv) >= 2:
    METADATA_DATFILE = sys.argv[2]

### Load data from disk ###

with open(META_FILE, 'r') as file:
    meta = json.load(file)
with open(GENRES_LIST_FILE, 'r') as file:
    genres = json.load(file)
with open(ARTISTS_LIST_FILE, 'r') as file:
    artists = json.load(file)


### Write file names ###

with open(FILENAMES_DATFILE, 'w') as file:
    for datum in meta:
        file.write(os.path.abspath(datum['wav_file']))
        file.write('\n')

with open(METADATA_DATFILE, 'w') as file:
    for song in meta:
        file.write('%i ' % genres.index(song['genre']))
        for artist in artists:
            if artist in song['artists']:
                file.write('1 ')
            else:
                file.write('0 ')
        file.write('\n')

