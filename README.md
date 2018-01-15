
# minimalPairGenerator
this takes in an audio transcript and the audio and outputs audio files of the minimal pairs


eventual dir structure:
```
  base
    |__original_audio
    |__converted_audio
    |__transcripts
    |__json
    |__pairs
    |__data
        |__subdirs(based off transcript file names...though eventually based off of minimal pair distinctions, eg a-e)
            |__bat-bet
                 |__audio files for bat-bet across videos
            |__sat-set
                 |__audio files for sat-set across videos
            |__etc...
```

example steps not included in this particular repo:

- find youtube video (or youtube channel)

- grab audio from that video

- grab transcript from that video

--------------------------------------------------------------
below this line is where the pipeline is decoupled from the data source

- convert the webm files to mp3
(useful if the source files are from youtube)
  convert_to_mp3.py

- more cleaning of transcripts (this plus previous two should be combined into one step) and remove parentheses
  clean_transcripts.sh

- convert transcripts to just single lines (easier to parse) and filter for bad words
  convert_transcripts_to_single_lines.py

- generate list of minimal pairs per transcript
(this step is where meta-data about which phonemes differ can be generated...and then used as folder names. In each of these folders, the eventual minimal pair audio files will be labelled with the video name, so that they remain distinct even with multiple minimal pair audio files in a folder)
  get_pairs.py


- spin up a docker container with the "gentle" force-alignment server
create_fa_container.sh


- get force-aligned json file
(this is the step that takes the most time)
  force-align.sh

- grab each word as a separate audio file
(this also attempts to slow down all audio files by 50%)
  create_audio_files.py

- generate json file reflecting directory structure as well as audio sprites
(this is what will be sent to the front end to describe the location of each of the compiled audio files)
  generate_assets.py_
