#!/usr/bin/python

import sys
import os
import json

META_FILE = 'meta.json'
ARTISTS_LIST_FILE = 'artists.json'

if os.path.exists(META_FILE):
    with open(META_FILE, 'r') as meta_file:
        meta = json.load(meta_file)
else:
    meta = []

if os.path.exists(ARTISTS_LIST_FILE):
    with open(ARTISTS_LIST_FILE, 'r') as file:
        artists = json.load(file)
else:
    artists = []

for datum in meta:
    for artist in datum['artists']:
        if artist not in artists:
            artists.append(artist)

# save artists file
with open(ARTISTS_LIST_FILE, 'w') as file:
    json.dump(artists, file, sort_keys=True, indent=4, separators=(',', ': '))

