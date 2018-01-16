
# minimalPairGenerator
this takes in an audio transcript and the audio and outputs audio files of the minimal pairs


eventual dir structure:
```
  base
    |__converted_audio
    |__converted_transcripts
    |__data
    |   |__subdirs(based off of minimal pair distinctions, eg a-e)
    |       |__bat-bet
    |            |__audio files for bat-bet across videos
    |       |__sat-set
    |            |__audio files for sat-set across videos
    |       |__etc...
    |__force_aligned_json
    |__minimal_pairs
    |__original_audio
    |__original_transcripts
```

example steps not included in this particular repo:

- find youtube video (or youtube channel)

- grab audio from that video

- grab transcript from that video

--------------------------------------------------------------
below this line is where the pipeline is decoupled from the data source

1. clean up file names (replace everything with underscores, etc)
(TODO...this makes all the other file manipulation easier later)

`clean_file_names.py`

2. convert the webm files to mp3
(useful if the source files are from youtube)

`convert_to_mp3.py`

3. more cleaning of transcripts and removing parentheses

`clean_transcripts.py`

4. convert transcripts to just single lines (easier to parse) and filter for bad words

`convert_transcripts_to_single_lines.py`

5. generate list of minimal pairs per transcript
(this step is where meta-data about which phonemes differ can be generated...and then used as folder names. In each of these folders, the eventual minimal pair audio files will be labelled with the video name, so that they remain distinct even with multiple minimal pair audio files in a folder)

`get_pairs.py`


6. spin up a docker container with the "gentle" force-alignment server (TODO)

`create_fa_container.sh`


7. get force-aligned json file
(this is the step that takes the most time)

`force-align.py`

8. use force-alignment data to grab each word as a separate audio file from the original full audio
(this also attempts to slow down all audio files by 50%)

`create_audio_files.py`

9. generate json file reflecting directory structure as well as audio sprites
(this is what will be sent to the front end to describe the location of each of the compiled audio files)

`generate_assets.py`

------------------------------------------------------------------

## external dependencies
beyond python, the current pipeline relies on two external programs:

-ffmpeg (add installation instructions)

-waudsprite (add installation instructions with preference for nvm)

-docker (add installation instructions)
