# mTEDx_auxiliary

These are different files I created to do different tasks when I was working on creating ASR model for [mTEDx dataset](http://www.openslr.org/100). The following is a description of the different files you can find in this repo:

- `download_mted.sh`: A bash script to download the ASR part of the mTEDx dataset.
- `process_mtedx`: A file to process the mTEDx dataset. By processing, I mean:
    - Split the audio of the ted talks found in the datasets into shorter segments that can be used for training ASR models.
    - Normalizes the audio files to a sample rate of`16000` and number of channels of `1`.
    - Align between the audio segments and the text.
- `stats.xlsx`: An excel file gathering all the details of the data found in the dataset.


