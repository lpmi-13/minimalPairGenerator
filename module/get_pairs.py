#!/bin/python3
# _*_ coding: UTF-8 _*_
import distance
import epitran
import re
import os
import json
from itertools import combinations
from collections import defaultdict

CONVERTED_TRANSCRIPT_DIR = './converted_transcripts'
PAIRS_DIR = './minimal_pairs'
VOWEL_PHONEMES = {'æ', 'ɪ', 'ɑ', 'ʌ', 'ʊ', 'ɛ', 'i', 'ɔ', 'u', 'o','a', 'ə', 'e'}

if not os.path.exists(PAIRS_DIR):
    os.mkdir(PAIRS_DIR)

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

def is_minimal_pair(first, second):
    '''
    returns true if the two words passed in are minimal pairs.
    eg, big/bag. in the IPA format, and in the regular English
    spelling, both are different in the character used in the
    second position in the word.
    As a less obvious example, live/leave are also minimal
    pairs, because in the IPA, they are identical except for 
    the character in second position, whereas in the English
    spelling, there are differences in the second, third, and
    fourth characters
    '''
    return len(first) == len(second) and distance.hamming(first, second) == 1

def get_different_phoneme_index(word1, word2):
    '''
    this returns the index at which the two IPA formats are different
    '''
    difference_index = [i for i in range(len(word1)) if word1[i] != word2[i]]
    return difference_index[0]


def get_phoneme_pair(firstIPA, secondIPA):
    """
    this gets the actual two phonemes that differ and
    returns the character index in the IPA representations
    where this occurs
    """
    char_index = get_different_phoneme_index(firstIPA, secondIPA)
    encoding_pair = firstIPA[char_index] + '-' + secondIPA[char_index]
    return encoding_pair


def generate_folder_name(word_pair):
    return word_pair[0] + '-' + word_pair[1]


for filename in converted_transcript_files:

    with open(os.path.join(CONVERTED_TRANSCRIPT_DIR,filename), 'r') as f:
        text = f.readlines()

    '''
    this basically gets rid of all the stuff that isn't lowercase letters or apostrophes in possessives, and also filters blank lines
    '''
    wordArray = sorted(set([re.sub('[^a-z\']+', '', word.lower()) for word in text if word.strip() != '']))
 
    wordPhoneDict = defaultdict(None)
 
    #this creates a mapping between the word and the phonemes
    for word in wordArray:
        wordPhoneDict[word] = epi.transliterate(word)
 
    minimalPairDict = defaultdict(int)
 
    minimalPairArray = []
 
    # this part compares every word to every other word
    for firstWord, secondWord in combinations(wordPhoneDict, 2):

        '''
        we need this in order to make sure the order of
        the phonemes is the same as the order of the words
        (eg, i-e...sit-set)
        '''
        wordPair = alphabetize(firstWord, secondWord)

        firstIPA, secondIPA = wordPhoneDict[wordPair[0]], wordPhoneDict[wordPair[1]]

        if is_minimal_pair(firstIPA, secondIPA):

            phoneme_pair = get_phoneme_pair(firstIPA, secondIPA)
            phonemes = [phon for phon in phoneme_pair.split('-')]
            if (phonemes[0] in VOWEL_PHONEMES) and (phonemes[1] in VOWEL_PHONEMES):
                ordered_pair = generate_folder_name(wordPair)

                '''
                this maps the actual phoneme pair to the pair of
                words, though at some point, we may want to either
                lock down which pairs are legal to generate or 
                just filter all the phoneme pairs that aren't either
                vowel-vowel or consonant-consonant.
                eg, we're seeing stuff like 'e-k', which is bizarre
                and shouldn't be happening.
                I blame the hamming.distance function and will have
                to create some better testing around it, or just
                hack the source code
                '''
 
                minimalPairDict[ordered_pair] = phoneme_pair

    # we invert the dict to get a json representation of the eventual directory structure

    json_data = dict_invert(minimalPairDict)

    print(json_data)

    new_filename_json = '{}-minimal_pairs.json'.format(filename)

    with open(os.path.join(PAIRS_DIR,new_filename_json),'w') as json_output:
        json.dump(json_data, json_output)
   
    print('finished processing {}'.format(filename))
