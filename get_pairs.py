import distance
import epitran
import re
import os
import yaml
import json
from itertools import combinations
from collections import defaultdict

CONVERTED_TRANSCRIPT_DIR = './converted_transcripts/'
PAIRS_DIR = './minimal_pairs/'

epi = epitran.Epitran('eng-Latn')

converted_transcript_files = os.listdir(CONVERTED_TRANSCRIPT_DIR)

def alphabetize(firstWord, secondWord):
    words = [firstWord, secondWord]
    words.sort()
    return words

def dict_invert(d):
    inv = {}
    for k, v in d.items():
        keys = inv.setdefault(v, [])
        keys.append(k)
    return inv

def get_diff(first, second):
    if len(first) == len(second):
        return distance.hamming(first, second)

def get_different_phoneme(word1, word2):
    difference_index = [i for i in range(len(word1)) if word1[i] != word2[i]]
    return difference_index[0]

for filename in converted_transcript_files:

    with open(os.path.join(CONVERTED_TRANSCRIPT_DIR,filename), 'r') as f:
        text = f.readlines()

    '''
    this basically gets rid of all the stuff that isn't lowercase letters or apostrophes in possessives, and also filters blank lines
    '''
    wordArray = set([re.sub('[^a-z\']+', '', word.lower()) for word in text if word.strip() != ''])
 
    wordPhoneDict = defaultdict(None)
 
    #this creates a mapping between the word and the phonemes
    for word in wordArray:
        wordPhoneDict[word] = epi.transliterate(word)
 
    minimalPairDict = defaultdict(int)
 
    minimalPairArray = []
 
    for firstWord, secondWord in combinations(wordPhoneDict, 2):

        '''
        we need this in order to make sure the order of
        the phonemes is the same as the order of the words
        (eg, i-e...sit-set)
        '''
        wordPair = alphabetize(firstWord, secondWord)

        firstIPA, secondIPA = wordPhoneDict[wordPair[0]], wordPhoneDict[wordPair[1]]

        if get_diff(firstIPA, secondIPA) == 1:

            #gets the actual two phonemes that differ
            char_index = get_different_phoneme(firstIPA, secondIPA)
            encoding_pair = firstIPA[char_index] + '-' + secondIPA[char_index]
            # use this to generate folder names
            ordered_pair = wordPair[0] + '-' + wordPair[1]

            #this maps each word pair to a phoneme diff pair
            minimalPairDict[ordered_pair] = encoding_pair

    # we invert the dict to get a json representation of the eventual directory structure
    json_data = dict_invert(minimalPairDict)

    print(json_data)

    new_filename_json = '{}-minimal_pairs.json'.format(filename)

    with open(os.path.join(PAIRS_DIR,new_filename_json),'w') as json_output:
        json.dump(json_data, json_output)
   
 
    print('finished processing {}'.format(filename))
