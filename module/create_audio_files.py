import subprocess
import os
import json

DATA_DIR = './data/'
FORCE_ALIGNED_DIRECTORY = './force_aligned_json/'
PAIRS_DIRECTORY = './minimal_pairs/'

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

json_files = os.listdir(PAIRS_DIRECTORY)

for filename in json_files:
    char_index = filename.find('.txt')
    short_name = filename[:char_index]

    # this is the minimal pairs data
    with open(os.path.join(PAIRS_DIRECTORY, filename), 'r') as f:
        data = json.load(f)

    with open(os.path.join(FORCE_ALIGNED_DIRECTORY, short_name + '.json'), 'r') as w:
        # loads the force-alignment results per video
        fa_data = json.load(w)
        fa_words = fa_data['words']

    for pair_key in data:

        subdir = DATA_DIR + pair_key

        '''
        this is where we will make a subdirectory under /data/
        named for each phoneme pair in the json file for this
        video
        '''
        if not os.path.exists(subdir):
            os.mkdir(subdir)

        for item in data[pair_key]:

            '''
            this is where we make subdirectories under the phoneme
            pair for each word pair we will have audio files for
            '''
            sub_subdir = subdir + '/' + item

            if not os.path.exists(sub_subdir):
                os.mkdir(sub_subdir)

            # split the word pair into two words
            for pair_word in item.split('-'):

                created_flag = False

                for aligned_word in fa_words:

                    '''
                    this is where we eventually want to filter
                    based on the length of the audio for the
                    word. Initial rough testing suggests a length
                    of below 0.4 seconds is probably too short
                    to be intelligible, even for vowels
                    '''
                    if (aligned_word['word'] == pair_word
                    and aligned_word['case'] == 'success'
                    and created_flag is False):


                        f_path = subdir + item + aligned_word['word']
                        print('creating file for {}'.format(f_path))
                        start_time = str(aligned_word['start'])
                        end_time = str(aligned_word['end'])
                        tot_time = aligned_word['end'] - aligned_word['start']
                        duration = str(tot_time)
                        word = aligned_word['word']

                        command = [
                            'ffmpeg',
                            '-ss',
                            start_time,
                            '-i',
                            './converted_audio/' + short_name + '.mp3',
                            '-t',
                            duration,
                            # the next three lines slow down by 50%
                            '-filter:a',
                            'atempo=.50',
                            '-vn',
                            sub_subdir + '/' + short_name + '_' + word + '.mp3'
                        ]
                        created_flag = True

                        subprocess.call(command)
