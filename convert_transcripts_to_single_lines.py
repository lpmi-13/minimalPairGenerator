import os
from stoplist import bad_words

TRANSCRIPT_DIR = './original_transcripts'
SINGLE_LINE_DIR = './converted_transcripts'

for filename in os.listdir(TRANSCRIPT_DIR):
    with open(os.path.join(TRANSCRIPT_DIR,filename), 'r') as f:
        text = f.readlines()

    with open(os.path.join(SINGLE_LINE_DIR,filename), 'w') as output:
        for line in text:
            wordArray = line.split(' ')
            for word in wordArray:
                output.write(word + '\n') if word not in bad_words
