import os
import subprocess
import sys

DOCKER_PORT = sys.argv[1]

CONVERTED_AUDIO_DIR = 'converted_audio/'
CONVERTED_TRANSCRIPT_DIR = 'converted_transcripts/'
FORCE_ALIGNMENT_JSON_DIR = 'force_aligned_json/'

if not os.path.exists(FORCE_ALIGNMENT_JSON_DIR):
    os.mkdir(FORCE_ALIGNMENT_JSON_DIR)

for audio_file in os.listdir(CONVERTED_AUDIO_DIR):
    filename, file_extension = os.path.splitext(audio_file)

    curl_command = ['curl', '-F', 'audio=@' + os.path.join(CONVERTED_AUDIO_DIR, audio_file), '-F', 'transcript=@' + os.path.join(CONVERTED_TRANSCRIPT_DIR, filename + '.txt'), 'http://127.0.0.1:' + DOCKER_PORT + '/transcriptions?async=false', '-o', os.path.join(FORCE_ALIGNMENT_JSON_DIR, filename + '.json')]

    subprocess.call(curl_command)
