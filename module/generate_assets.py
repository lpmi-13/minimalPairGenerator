import json
import os
import subprocess

DATA_DIR = './data/'
VOWEL_PHONEMES = {'æ', 'ɪ', 'ɑ', 'ʌ', 'ʊ', 'ɛ', 'i', 'ɔ', 'u', 'o','a', 'ə', 'e'}

directory_json = {}

for subdir in os.listdir(DATA_DIR):
    directory_path = DATA_DIR + subdir

    json_item = {'words' : []}

    pair_directories = os.listdir(directory_path)

    for sub_subdir in pair_directories:

        # build up the json describing the directory structure
        json_item['words'].append(sub_subdir)

        # generate the compiled audio assets
        sounds_dir = DATA_DIR + subdir + '/' + sub_subdir + '/'
        print('sounds dir is: {}'.format(sounds_dir))
        m4a_file_name = sounds_dir + sub_subdir
        print('m4a file name is: {}'.format(m4a_file_name))

        command = ['waudsprite', '--loop', 'loop', '--autoplay', 'loop', '-o', m4a_file_name, '-e', 'm4a', sounds_dir + '*.mp3']
        print('attempting {}'.format(command))

        subprocess.call(command)

    directory_json[subdir] = json_item

with open('directory.json','w') as f:
    json.dump(directory_json, f)
