import subprocess
import os
import json
from jsonpath_rw import jsonpath, parse

DATA_DIR = './data/'
FORCE_ALIGNED_DIRECTORY = './force_aligned_json/'
PAIRS_DIRECTORY = './minimal_pairs/'

jsonpath_expr = parse('words[*].alignedWord')

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

json_files = os.listdir(PAIRS_DIRECTORY)

for filename in json_files:
    print('working on file: {}'.format(filename))
    char_index = filename.find('.txt')
    short_name = filename[:char_index]
    print('short name is: {}'.format(short_name))

    # this is the minimal pairs data
    with open(os.path.join(PAIRS_DIRECTORY, filename), 'r') as f:
        data = json.load(f)

    with open(os.path.join(FORCE_ALIGNED_DIRECTORY, short_name + '.json'), 'r') as w:
        # loads the force-alignment results per video
        fa_data = json.load(w)
        fa_words = fa_data['words']

    for pair_key in data:

        for item in data[pair_key]:

            # split the word pair into two words
            for pair_word in item.split('-'):

                '''
                so we're getting output files that only have one
                of the two minimal pairs because the first one
                lasts longer than .5 seconds, but the second one
                doesn't...so we need to check to make sure both of them
                are over .5...

                this will possibly matter less when the data set 
                is much bigger. But at any rate, probably not too 
                terrible if we only have one of the words, just
                since it's another opportunity to hear the sound
                '''

                created_flag = False

                for aligned_word in fa_words:

                    #print('checking aligned_word {}'.format(aligned_word))
                    '''
                    we still need to check that both of the words
                    forming the minimal pair have sound clips
                    over 0.5 seconds. This is currently only
                    checking one of them.
                    '''
                    if (aligned_word['word'] == pair_word
                    and aligned_word['case'] == 'success'
                    and created_flag is False):
                        
                        tot_time = aligned_word['end'] - aligned_word['start']
                        print('tot_time is {} for word {}'.format(tot_time, aligned_word['word']))
                        if tot_time > 0.5:

                            subdir = DATA_DIR + pair_key + '/'

                            if not os.path.exists(subdir):
                                os.mkdir(subdir)
                                '''
                                this is where we make subdirectories under the phoneme
                                pair for each word pair we will have audio files for
                                '''
                            sub_subdir = subdir + '/' + item + '/'
                
                
                            '''
                            this is also where we are creating directories
                            before checking that we will have sounds that are
                            long enough to be put in those directories...perhaps
                            put this directory creation after the duration check
                            '''
                
                            if not os.path.exists(sub_subdir):
                                os.mkdir(sub_subdir)
                

                            start_time = str(aligned_word['start'])
                            end_time = str(aligned_word['end'])
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

                            print('running command: {}'.format(command))
                            subprocess.call(command)

                            '''
                            this is where we will make a subdirectory under /data/
                            named for each phoneme pair in the json file for this
                            video
                            '''

