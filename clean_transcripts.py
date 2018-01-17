import os
import subprocess

ORIGINAL_TRANSCRIPT_DIR = './original_transcripts/'

'''
will eventually transition this into pure python regex,
but leaving in the original sed for now
'''

for transcript in os.listdir(ORIGINAL_TRANSCRIPT_DIR):
    sed_command_parentheses = ['sed', '-i', 's/[(.+)]//g', ORIGINAL_TRANSCRIPT_DIR + transcript]

    subprocess.call(sed_command_parentheses)

    sed_command_title = ['sed', '-i', '/Title:/d', ORIGINAL_TRANSCRIPT_DIR + transcript]

    subprocess.call(sed_command_title)
