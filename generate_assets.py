import json
import os
import subprocess

DATA_DIR = './data/'

directory_json = {}

for subdir in os.listdir(DATA_DIR):
    directory_path = DATA_DIR + subdir

    keys = directory_json.setdefault(subdir, [])

    pair_directories = os.listdir(directory_path)

    for sub_subdir in pair_directories:

        # build up the json describing the directory structure
        keys.append(sub_subdir)

        # generate the compiled audio assets
        sounds_dir = DATA_DIR + subdir + '/' + sub_subdir + '/'
        m4a_file_name = sounds_dir + sub_subdir

        command = ['waudsprite', '--loop', 'loop', '--autoplay', 'loop', '-o', m4a_file_name, '-e', 'm4a', sounds_dir + '/*.mp3']

        subprocess.call(command)

with open('directory.json','w') as f:
    json.dump(directory_json, f)
