import os
import subprocess

AUDIO_DIR = './converted_audio/'
TRANSCRIPT_DIR = './converted_transcripts/'
FORCE_ALIGNMENT_JSON_DIR = './force_aligned_json/'

'''
research the way to get the process ID of the locally running docker container with the gentle force-alignment service running
'''

if not os.path.exists(FORCE_ALIGNMENT_JSON_DIR):
    os.mkdir(FORCE_ALIGNMENTS_JSON_DIR)

'''
I assume this subprocess command will complete synchronously
given that the query param explicitly specifies async=false...
but haven't actually tried it yet via python subprocess
'''
for audio_file in os.listdir(AUDIO_DIR):
    filename, file_extension = os.path.splitext(audio_file)

    curl_command = ['curl', '-F', '"audio=@' + AUDIO_DIR + '/' + audio_file + '"', '-F', '"transcript=@' + TRANSCRIPT_DIR + filename + '.txt"', '"http://localhost:' + docker_ps_id + '/transcriptions?async=false"', '-v', '>', '"' + FORCE_ALIGNEMENT_JSON_DIR + filename + '.json"'] 
