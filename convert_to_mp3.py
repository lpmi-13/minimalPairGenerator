import os
import subprocess

ORIGINAL_AUDIO_DIR = './original_audio/'
CONVERTED_AUDIO_DIR = './converted_audio/'

audio_dir = os.listdir(ORIGINAL_AUDIO_DIR)

if not os.path.exists(CONVERTED_AUDIO_DIR):
    os.mkdir(CONVERTED_AUDIO_DIR)

for audio_file in audio_dir:
    filename, file_extension = os.path.splitext(audio_file)

    '''
    not actually sure if this will convert anything to mp3,
    since only tested with webm, but theoretically could work
    '''
    command = ['ffmpeg', '-i', ORIGINAL_AUDIO_DIR + audio_file, '-acodec', 'libmp3lame', '-aq', '2', CONVERTED_AUDIO_DIR + '/' + filename + '.mp3']

    subprocess.call(command)
