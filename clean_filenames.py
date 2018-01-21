import os, re

ORIGINAL_AUDIO_DIR = './original_audio'
ORIGINAL_TRANSCRIPT_DIR = './original_transcripts'

def clean_filename(title):
    rep = {"/": "-", ":": "-", "\\": "-", "<": "-", ">": "-", "|": "-", "?": "", "*": "", "\"": "", " ": "_", "'": "", "!": "", ",": ""}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))

    return pattern.sub(lambda m: rep[re.escape(m.group(0))], title)


for audio_track in os.listdir(ORIGINAL_AUDIO_DIR):
    os.rename(os.path.join(ORIGINAL_AUDIO_DIR,audio_track), os.path.join(ORIGINAL_AUDIO_DIR, clean_filename(audio_track)))

for transcript in os.listdir(ORIGINAL_TRANSCRIPT_DIR):
    os.rename(os.path.join(ORIGINAL_TRANSCRIPT_DIR,transcript), os.path.join(ORIGINAL_TRANSCRIPT_DIR, clean_filename(transcript)))
