
# minimalPairGenerator
this takes in an audio transcript and the audio and outputs audio files of the minimal pairs

## background - what are minimal pairs?

TL;DR - two words with only one meaningful sound difference (these differences can vary between different languages). This becomes very obvious once the usual written form of a language is converted into [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet), which has the benefit of representing one unique sound with one unique symbol. So for language learners from a background of fewer vowel phonemes than English (eg, Spanish), some vowels sound the same to them, and are very difficult to distinguish in conversation.

examples:

- peach / pitch
  pit͡ʃ  / pɪt͡ʃ

- breath / bread
  bɹɛθ / bɹɛd

- peer / fear
  pɪɹ  / fɪɹ

...for a bit less of an overview, [this paper](https://journals.equinoxpub.com/index.php/CALICO/article/viewFile/22985/18991) outlines why practicing minimal pairs can be beneficial in the context of second language acquisition, and specifically describes a method involving learners listening to minimal pairs spoken by multiple different speakers.


## why automate it?

The only current applications (that I'm aware of) rely on actual humans to record themselves saying these minimal pairs and submitting them to the system. This has obvious disadvantages in terms of scalability, since even the kind souls dedicated enough to submit their own voice recordings probably don't have a very large amount of time to devote to the task.

Fortunately, automatic speech recognition (while still not great), is good enough for us to use in force alignment, which outputs the time-stamp location of every word in an audio stream (It can actually output time stamps for every phoneme, but we don't need that level of detail here).

Based on the list of minimal pairs present in the video (which we calculate from the transcript), we can then use the force alignment time-stamps to pull out just the audio that has each half of each minimal pair and save those to separate audio files.

At the end of the process, we concatenate all the audio for all the speakers for one particular minimal pair, and with enough input data (I'm aiming for 800 audio/transcript pairs), we should have a fair amount of variation in speakers/accents for a large number of minimal pairs.


## to run
`bash generate.sh`

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
below this line is where the pipeline is decoupled from the data source. This is what `generate.sh` runs, in this sequence:

1. clean up file names (replace everything with underscores, etc)

`clean_filenames.py`


2. convert the webm files to mp3
(useful if the source files are from youtube)

`convert_to_mp3.py`


3. cleaning of transcripts to removing parentheses, titles, and bad words, as well as reformatting to be one word per line

`clean_and_convert_transcripts.py`

***
THESE FIRST THREE STEPS ARE EXPECTING TO FIND
`original_audio/`
AND
`original_transcripts/`
AS DIRECTORIES.

...I will eventually refactor stuff to make it accept command line arguments for whatever input folder you want, but just focused on getting it all working at the moment
***

4. generate list of minimal pairs per transcript
(this step is where meta-data about which phonemes differ can be generated...and then used as folder names. In each of these folders, the eventual minimal pair audio files will be labelled with the video name, so that they remain distinct even with multiple minimal pair audio files in a folder)

`get_pairs.py`


5. spin up a docker container with the "gentle" force-alignment server 

`create_fa_container.sh`


6. get force-aligned json file
(this is the step that takes the most time)

`force-align.py`


7. use force-alignment data to grab each word as a separate audio file from the original full audio
(this also attempts to slow down all audio files by 50%)

`create_audio_files.py`


8. generate json file reflecting directory structure as well as audio sprites
(this is what will be sent to the front end to describe the location of each of the compiled audio files)

`generate_assets.py`


------------------------------------------------------------------

## external dependencies
beyond python, the current pipeline relies on three external programs:

-ffmpeg (add installation instructions)

-waudsprite (add installation instructions with preference for nvm)

-docker (add installation instructions)
