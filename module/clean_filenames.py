import os, re

ORIGINAL_AUDIO_DIR = './original_audio'
ORIGINAL_TRANSCRIPT_DIR = './original_transcripts'

def clean_filename(title):

    '''
    TODO - this is currently a list of all the characters 
    that we want to replace, but it should be a list of 
    characters that we don't want to replace, which would 
    be more robust (ie, just replace all spaces with underscores
    , and everything else thats not a lowercase letter with nothing
    '''
    rep = {"/": "-", ":": "-", "\\": "-", "<": "-", ">": "-", "|": "-", "?": "", "*": "", "\"": "", " ": "_", "'": "", "!": "", ",": ""}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))

    return pattern.sub(lambda m: rep[re.escape(m.group(0))], title)


for audio_track in os.listdir(ORIGINAL_AUDIO_DIR):
    os.rename(os.path.join(ORIGINAL_AUDIO_DIR,audio_track), os.path.join(ORIGINAL_AUDIO_DIR, clean_filename(audio_track)))

for transcript in os.listdir(ORIGINAL_TRANSCRIPT_DIR):
    os.rename(os.path.join(ORIGINAL_TRANSCRIPT_DIR,transcript), os.path.join(ORIGINAL_TRANSCRIPT_DIR, clean_filename(transcript)))
