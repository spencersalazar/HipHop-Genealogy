#!/usr/bin/python

import sys
import os
import json
import uuid
import mutagen


def getGenre(path):
    NUM_COLUMNS = 5
    genre = None
    
    while genre == None:
        line = raw_input("Select a genre (0-%i, [l]ist genres, show song [i]nfo): " % (len(genres)-1))
        
        try:
            num = int(line)
            if num >= 0 and num < len(genres):
                return genres[num]
        except:
            if line == 'l':
                for i in range(0,len(genres)):
                    print "%i: %s\t" % (i, genres[i]),
                    if i%NUM_COLUMNS == NUM_COLUMNS-1: print
                print
            elif line == 'i':
                tag = mutagen.File(path, easy=True)
                if 'title' in tag: print 'title: %s' % tag['title']
                if 'artist' in tag: print 'artist: %s' % tag['artist']
                if 'album' in tag: print 'album: %s' % tag['album']
                print

def getArtists(path):
    NUM_COLUMNS = 5    
    song_artists = []
    
    while True:
        line = raw_input("Add an artist (0-%i, or [l]ist artists, show song [i]nfo, [n]ew artist, [f]inish]): " % (len(artists)-1))
        try:
            num = int(line)
            if num >= 0 and num < len(artists):
                song_artists.append(artists[num])
        except:
            if line == 'l':
                for i in range(0, len(artists)):
                    print "%i: %s\t" % (i, artists[i]),
                    if i%NUM_COLUMNS == NUM_COLUMNS-1: print
                print
            elif line == 'i':
                tag = mutagen.File(path, easy=True)
                if 'title' in tag: print 'title: %s' % tag['title']
                if 'artist' in tag: print 'artist: %s' % tag['artist']
                if 'album' in tag: print 'album: %s' % tag['album']
                print
            elif line == 'n':
                line = raw_input('Enter artist name or [c]ancel: ')
                if line != 'c':
                    artists.append(line)
            elif line == 'f':
                return song_artists
        

META_FILE = 'meta.json'
GENRES_LIST_FILE = 'genres.json'
ARTISTS_LIST_FILE = 'artists.json'
COMPRESSED_DIR = 'compressed'


### Load data from disk ###

files = dict()

if os.path.exists(META_FILE):
    with open(META_FILE, 'r') as meta_file:
        meta = json.load(meta_file)
else:
    meta = []

with open(GENRES_LIST_FILE, 'r') as file:
    genres = json.load(file)

if os.path.exists(ARTISTS_LIST_FILE):
    with open(ARTISTS_LIST_FILE, 'r') as file:
        artists = json.load(file)
else:
    artists = []

for datum in meta:
    files[datum['compressed_file']] = datum


### Check metadata, request user input if needed ###

for root, _dirs, _files in os.walk(COMPRESSED_DIR):
    for file in _files:
        path = os.path.join(root, file)
        if path not in files:
            print "adding file '%s'" % file
            tag = mutagen.File(path, easy=True)
            if 'title' in tag: print 'title: %s' % tag['title']
            if 'artist' in tag: print 'artist: %s' % tag['artist']
            if 'album' in tag: print 'album: %s' % tag['album']
            print
                        
            datum = {}
            datum['uuid'] = uuid.uuid4().hex
            datum['compressed_file'] = path
            datum['genre'] = getGenre(path)
            datum['artists'] = getArtists(path)
            meta.append(datum)


### Save Data ###

# save metadata file
with open(META_FILE, 'w') as meta_file:
    json.dump(meta, meta_file, sort_keys=True, indent=4, separators=(',', ': '))

# save artists file
with open(ARTISTS_LIST_FILE, 'w') as file:
    json.dump(artists, file, sort_keys=True, indent=4, separators=(',', ': '))

