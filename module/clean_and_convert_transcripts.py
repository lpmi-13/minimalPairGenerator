import os
import subprocess
from stoplist import bad_words

ORIGINAL_TRANSCRIPT_DIR = './original_transcripts'
CONVERTED_TRANSCRIPT_DIR = './converted_transcripts'

if not os.path.exists(CONVERTED_TRANSCRIPT_DIR):
    os.mkdir(CONVERTED_TRANSCRIPT_DIR)

for transcript in os.listdir(ORIGINAL_TRANSCRIPT_DIR):

    '''
    this will eventually by converted to pure python regex
    but leaving in the basic sed syntax for now
    '''

    # this removes everything between parentheses in the transcript
    sed_command_remove_parentheses = ['sed', '-i', 's/[(.+)]//g', os.path.join(ORIGINAL_TRANSCRIPT_DIR, transcript)]

    subprocess.call(sed_command_remove_parentheses)

    # this removes the title at the top of the transcript
    sed_command_remove_title = ['sed', '-i', '/Title:/d', os.path.join(ORIGINAL_TRANSCRIPT_DIR, transcript)]

    subprocess.call(sed_command_remove_title)

    # converting transcripts to one word per line
    with open(os.path.join(ORIGINAL_TRANSCRIPT_DIR,transcript), 'r') as f:
        text = f.readlines()

    with open(os.path.join(CONVERTED_TRANSCRIPT_DIR,transcript), 'w') as output:
        for line in text:
            if line.strip() and ':' not in line:
                wordArray = line.split(' ')
                for word in wordArray:
                    if (word not in bad_words):
                        output.write(word + '\n')
