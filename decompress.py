#!/usr/bin/python

import sys
import os
import json
import subprocess

META_FILE = 'meta.json'
COMPRESSED_DIR = 'compressed'
WAV_DIR = 'wav'


### Load data from disk ###

if os.path.exists(META_FILE):
    with open(META_FILE, 'r') as meta_file:
        meta = json.load(meta_file)
else:
    meta = []

if not os.path.isdir(WAV_DIR):
    os.mkdir(WAV_DIR)


### Convert ###

num = 0

for datum in meta:
    if 'wav_file' not in datum or not os.path.exists(datum['wav_file']):
        print "converting '%s'" % datum['compressed_file']
        datum['wav_file'] = os.path.join(WAV_DIR, os.path.basename(os.path.splitext(datum['compressed_file'])[0] + '.wav'))
        code = subprocess.call(['ffmpeg', '-i', datum['compressed_file'], datum['wav_file']])
        if code != 0:
            print "error converting '%s'" % datum['compressed_file']
        else:
            num += 1

print "converted %i files" % num

# save metadata file
with open(META_FILE, 'w') as meta_file:
    json.dump(meta, meta_file, sort_keys=True, indent=4, separators=(',', ': '))

