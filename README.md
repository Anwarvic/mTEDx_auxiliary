# mTEDx_auxiliary

These are different files I created to do different tasks when I was working on creating ASR model for [mTEDx dataset](http://www.openslr.org/100). The following is a description of the different files you can find in this repo:

- `download_mted.sh`: A bash script to download the ASR part of the mTEDx dataset.
- `process_mtedx`: A file to process the mTEDx dataset. By processing, I mean:
    - Split the audio of the ted talks found in the datasets into shorter segments that can be used for training ASR models.
    - Normalizes the audio files to a sample rate of`16000` and number of channels of `1`.
    - Align between the audio segments and the text.
- `stats.xlsx`: An excel file gathering all the details of the data found in the dataset.


## How to download the data

You can download [mTEDx data](http://www.openslr.org/100) by running the
following [bash script](https://github.com/Anwarvic/mTEDx_auxiliary/blob/main/download_mtedx.sh):
```bash
bash download_mtedx.sh
```

## How the data should look like

After downloading the audio data, you need to process the audio data and split
the whole talks into different segments and align it with the correct text. 
All of that can be done by running this
[python script](https://github.com/Anwarvic/mTEDx_auxiliary/blob/main/process_mtedx.py)
like so:
```
python process_mtedx.py \
  --in [IN_DATA_PATH] \
  --out [OUT_DATA_PATH] \
  --langs [LANGS] \
  --groups [GROUPS]

```
For example:
```
python process_mtedx.py \
  --in /scratch/1/user/manwar/data/mTEDx_downloaded \
  --out /scratch/1/user/manwar/data/mTEDx \
  --langs ar fr \
  --groups test valid train
```

This will process all audio data and organize it in the following tree:
```text
mTEDx
├── ar
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
├── de
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
├── el
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
├── es
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
├── fr
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
├── it
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
├── pt
│   ├── test
│   ├── test.json
│   ├── train
│   ├── train.json
│   ├── valid
│   └── valid.json
└── ru
    ├── test
    ├── test.json
    ├── train
    ├── train.json
    ├── valid
    └── valid.json
```
