eventual dir structure:
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

...definitely need grouping by minimal pair. This will be relevant at the stage where we generate audio sprites (eg, based on the a-e directory, we need separate audiosprites for sat-set and bat-bet)...so we possibly want another subdir below the minimal pair subdir named the two words that will be in the sprite.


steps in the process:

find youtube video (or youtube channel)

grab audio from that video
  grab_audio.py

grab transcript from that video
(this is where we need to make sure the file name doesn't have any extra crap in it...quotations or weird chars)
  get_transcript.py

--------------------------------------------------------------
below this line is where the pipeline is decoupled from the data source

convert the webm files to mp3
  convert_to_mp3.py

more cleaning of transcripts (this plus previous two should be combined into one step) and remove parentheses
  clean_transcripts.sh

convert transcripts to just single lines (easier to parse) and filter for bad words
  convert_transcripts_to_single_lines.py

generate list of minimal pairs per transcript
(this step is where meta-data about which phonemes differ can be generated...and then used as folder names. In each of these folders, the eventual minimal pair audio files will be labelled with the video name, so that they remain distinct even with multiple minimal pair audio files in a folder)
  get_pairs.py


spin up a docker container with the "gentle" force-alignment server
create_fa_container.sh


get force-aligned json file
(this is the step that takes the most time)
  force-align.sh

grab each word as a separate audio file
(this also attempts to slow down all audio files by 50%)
  create_audio_files.py

generate json file reflecting directory structure as well as audio sprites
(this is what will be sent to the front end to describe the location of each of the compiled audio files)
  generate_assets.py_
