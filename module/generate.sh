#!/bin/bash
#### this is a script to stick together all the intermediate
#### processes that are used to convert transcript/audio pairings
#### into audio assets of minimal pairs
#### unfortunately, still requires root privileges to run

echo "cleaning up filenames..."
# gets rid of difficult characters
/usr/bin/python3 clean_filenames.py

echo "converting to mp3..."
/usr/bin/python3 convert_to_mp3.py

echo "cleaning up transcripts..."
# removes extra non-dialog parts from the transcript
# and converts the file to just one word per line
/usr/bin/python3 clean_and_convert_transcripts.py

echo "generating list of minimal pairs for each transcript..."
/usr/bin/python3 get_pairs.py

echo "starting docker container with force-alignment server..."
# fires up a docker container running the gentle force-alignment
# server, and makes sure it runs in the background so that the
# terminal output is still related to the processing of the
# files rather than the activity in the docker container, which
# is really boring and uninformative anyway
./create_fa_container.sh &>/dev/null &

echo "grabbing port assignment for force-alignment server..."
# sleeping here because this port resolution takes a bit of time
sleep 3
LOCAL_DOCKER_PORT="$(docker port $(docker ps -aq) | tail -c 6)"

echo "local docker port: $LOCAL_DOCKER_PORT"

echo "starting force alignment process..."
# this step takes a really long time (approx 7-10 minutes for a
# 14 Megabyte audio file)
/usr/bin/python3 force-align.py "$LOCAL_DOCKER_PORT"

echo "using force alignment data to create minimal pair audio files..."
/usr/bin/python3 create_audio_files.py

#comment out if not using node via nvm
source ~/.nvm/nvm.sh
nvm use node

echo "generating json metadata of directory structure..."
# this step uses waudsprite, which converts the single audio files
# in a particular directory (eg, sit-set) into one continuous 
# audio file of all the speakers who say that particular minimal
# pair 
/usr/bin/python3 generate_assets.py

echo "shutting down docker container"
docker stop "$(docker ps -aq)"

docker rm "$(docker ps -aq)"

printf "\n\n\nall done!"
printf "\n\n\ncompiled audio files in /data"
