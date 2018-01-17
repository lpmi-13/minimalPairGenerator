import os
from stoplist import bad_words

ORIGINAL_TRANSCRIPT_DIR = './original_transcripts/'
CONVERTED_TRANSCRIPT_DIR = './converted_transcripts/'

for filename in os.listdir(ORIGINAL_TRANSCRIPT_DIR):
    with open(os.path.join(ORIGINAL_TRANSCRIPT_DIR,filename), 'r') as f:
        text = f.readlines()

    with open(os.path.join(CONVERTED_TRANSCRIPT_DIR,filename), 'w') as output:
        for line in text:
            wordArray = line.split(' ')
            for word in wordArray:
                if (word not in bad_words):
                    output.write(word + '\n')
