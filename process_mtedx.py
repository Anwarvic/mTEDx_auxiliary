import os
import yaml
import json
import torch
import torchaudio
from tqdm import tqdm
from joblib import Parallel, delayed


def load_audio_text_data(data_folder, lang, group):
    """
    Parses YAML files found in the mTEDx dataset and returns audio and text
    samples.

    Arguments
    ---------
    data_folder: str
        The absolute/relative path to the directory where the audio file is
        located.
    lang : str
        The language code.
    group : list
        The group to be processed, e.g "test".
    """
    base_dir = (
        os.path.join(data_folder, f"{lang}-{lang}","data",group,"txt")
    )
    # parse YAML file containing audio info
    with open( os.path.join(base_dir, f"{group}.yaml"), "r") as fin:
        audio_samples = yaml.load(fin, Loader=yaml.Loader)
    # parse text file containing text info
    with open( os.path.join(base_dir, f"{group}.{lang}"), "r") as fin:
        text_samples = fin.readlines()
    # sanity check
    assert len(text_samples) == len(audio_samples), \
        f"Data mismatch with language: {lang}, group: {group}"
    
    return audio_samples, text_samples


def split_and_save_audio(input_path, output_path, start_time, end_time,
        input_sample_rate, out_sample_rate=16000):
    """
    Splits the given audio file into a segment based on the specified
    `start_time` & `end_time`. Then, it saves the audio segment in a mono wav
    format using `torchaudio`.

    Arguments
    ---------
    input_path: str
        The absolute/relative path to the directory where the audio file is
        located.
    output_path: str
        The absolute/relative path to the directory where the processed audio
        file will be located.
    start_time: float
        The start time of the audio segment.
    end_time: float
        The end time of the audio segment.
    input_sample_rate: int
        The input sample rate of the input audio file.
    out_sample_rate: int
        The output sample rate of the output audio segment (default: 16000).
    """
    # read the audio file
    audio_segment, _ = torchaudio.load(
        input_path,
        num_frames = int((end_time - start_time)*input_sample_rate),
        frame_offset = int(start_time*input_sample_rate)
    )
    # change the sample rate if needed
    resampled = torchaudio.transforms.Resample(
        input_sample_rate, out_sample_rate,
    )(audio_segment)
    # change the signal to mono (1 channel)
    audio_segment_mono = torch.mean(resampled, dim=0, keepdim=True)
    # save audio file
    torchaudio.save(output_path, audio_segment_mono, out_sample_rate)


def process_audio_text_sample(i, audio, text, data_folder, save_folder,
        lang, group):
    """
    Process one data sample.

    Arguments
    ---------
    i: int
        The index of the audio file.
    audio: dict
        A dictionary describing info about the audio segment like:
        speaker_id, duration, offset, ... etc.
    text: str
        The text of the audio segment.
    data_folder: str
        The absolute/relative path where the mTEDx data can be found.
    save_folder: str
        The absolute/relative path where the mTEDx data will be saved.
    
    Returns
    -------
    dict:
        A dictionary of audio-text segment info. 
    """
    audio_input_filepath = (
        f"{data_folder}/{lang}-{lang}/data/{group}/wav/{audio['speaker_id']}.flac"
    )
    audio_segment_filename = audio["speaker_id"]+f"_{i:04d}"
    audio_output_filepath = (
        f"{save_folder}/{lang}/{group}/{audio_segment_filename}.wav"
    )
    # save audio file
    info = torchaudio.info(audio_input_filepath)
    split_and_save_audio(
        audio_input_filepath,
        audio_output_filepath,
        audio["offset"],
        audio["offset"]+audio["duration"],
        info.sample_rate,
        OUT_SAMPLE_RATE
    )
    # create json file
    return {
        audio_segment_filename: {
            "wav": {
                "file": "{data_root}/" + f"{lang}/{group}/{audio_segment_filename}.wav",
                "start": audio["offset"],
                "end": audio["offset"]+audio["duration"],
            },
            "words": text.strip(),
            "duration": audio["duration"],
            "lang": lang,
        }
    }


def preprocess(data_folder, save_folder, lang, group):
    """
    Preprocess the mTEDx data found in the given language and the given group.
    Also, it writes the audio-text information in a json file.

    Arguments
    ---------
    data_folder : str
        Path to the folder where the original mTEDx dataset is stored.
    save_folder : str
        Location of the folder for storing the csv.
    lang : str
        The language code.
    group : list
        The group to be processed, e.g "test".
    """
    os.makedirs(save_folder, exist_ok=True)
    lang_folder = os.path.join(save_folder, lang)
    os.makedirs(lang_folder, exist_ok=True)
    os.makedirs(os.path.join(lang_folder, group), exist_ok=True)
    
    # Setting path for the json file
    json_file = os.path.join(lang_folder, f"{group}.json")
    # skip if the file already exists
    if os.path.exists(json_file):
        print(f"{json_file} already exists. Skipping!!")
        return
    
    print(f"Creating json file in {json_file} for {lang}, group: {group}")
    audio_samples, text_samples = load_audio_text_data(data_folder, lang, group)
    # combine text & audio information
    result = Parallel(n_jobs=os.cpu_count(), backend="threading")(
        delayed(process_audio_text_sample)
        (i, audio, text, data_folder, save_folder, lang, group) \
        for i, (audio, text,) in tqdm(
            enumerate(zip(audio_samples, text_samples)),
            desc=f"Processing {lang}, {group}",
            total = len(audio_samples)
        )
    )
    group_data = dict((key, val) for k in result for key, val in k.items())
    
    # write dict into json file    
    with open(json_file, 'w', encoding='utf8') as fout:
        fout.write(json.dumps(group_data, indent=4, ensure_ascii=False))
    print(f"{json_file} successfully created!")


def main(args):
    """
    Main function that iterates over all languages and groups to process
    the audio data.
    """
    for lang in args["langs"]:
        for group in args["groups"]:
            preprocess(args["in"], args["out"], lang, group)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', type=str, required=True,
                help='The absolute/relative path where the downloaded mTEDx'+ \
                    'data are located.')
    parser.add_argument('--out', type=str, required=True,
                help='The absolute/relative path where the processed mTEDx'+ \
                    'data will be located.')
    parser.add_argument('--langs', nargs='+', required=True,
                help='List of language codes separated by space, eg "de fr"')
    parser.add_argument('--groups', nargs='+', default="test valid train",
                help='List of groups separated by space, e.g. "valid train".')
    parser.add_argument('--out_samplerate', type=int, default=16000,
                help='The sample rate of the output audio files.')
    # parse arguments
    args = vars(parser.parse_args())

    # Global variable
    OUT_SAMPLE_RATE = args["out_samplerate"]

    # process the data
    main(args)
