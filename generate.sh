#!/bin/bash

echo "cleaning up filenames..."
/usr/bin/python3 clean_filenames.py

echo "converting to mp3..."
/usr/bin/python3 convert_to_mp3.py

echo "cleaning up transcripts..."
/usr/bin/python3 clean_and_convert_transcripts.py

echo "generating list of minimal pairs for each transcript..."
/usr/bin/python3 get_pairs.py

echo "starting docker container with force-alignment server..."
./create_fa_container.sh &>/dev/null &

echo "grabbing port assignment for force-alignment server..."
sleep 3
LOCAL_DOCKER_PORT="$(docker port $(docker ps -aq) | tail -c 6)"

echo "local docker port: $LOCAL_DOCKER_PORT"

echo "starting force alignment process..."
/usr/bin/python3 force-align.py "$LOCAL_DOCKER_PORT"

echo "using force alignment data to create minimal pair audio files..."
/usr/bin/python3 create_audio_files.py

#comment out if not using node via nvm
source ~/.nvm/nvm.sh
nvm use node

echo "generating json metadata of directory structure..."
/usr/bin/python3 generate_assets.py

echo "shutting down docker container"
docker stop "$(docker ps -aq)"

docker rm "$(docker ps -aq)"

echo "\n\n\nall done!"
echo "\n\n\ncompiled audio files in /data"
