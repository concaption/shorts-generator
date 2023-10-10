"""
This file contains utility functions for the project.
"""

import json
import os
import sys
import wave

import numpy as np
from pydub import AudioSegment


def load_config():
    """
    Loads the config files and returns the config object.
    """

    # Load the public config file
    with open("config/settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    # Load the private config file
    try:
        with open("config/settings_private.json", "r", encoding="utf-8") as f:
            private_config = json.load(f)
        config.update(private_config)
    except FileNotFoundError:
        print("No private config file found. Continuing with public config.")
    return config


class Config:
    """
    Class for storing the config object.
    """

    def __init__(self):
        try:
            settings = load_config()
            self.elevenlabs_api_key = settings["api"]["eleven_labs"].get("API_KEY")
            self.elevenlabs_voice = settings["api"]["eleven_labs"].get("voice")
            self.elevenlabs_model = settings["api"]["eleven_labs"].get("model")

            self.youtube_id = settings["api"]["youtube"].get("id")
            self.youtube_secret_key = settings["api"]["youtube"].get("secret_key")

            self.frame_size = tuple(settings["video_settings"].get("frame_size"))
            self.fps = settings["video_settings"].get("fps")
            self.music_proportion = settings["video_settings"].get("music_proportion")

            self.subtitle_pos = settings["video_settings"]["subtitle"].get("y_pos")
            self.subtitle_nb_word = settings["video_settings"]["subtitle"].get(
                "nb_word"
            )
            self.subtitle_nb_word_per_line = settings["video_settings"]["subtitle"].get(
                "nb_word_per_line"
            )
            self.subtitle_font = settings["video_settings"].get("font")
            self.subtitle_font_size = settings["video_settings"]["subtitle"].get(
                "font_size"
            )
            self.fade_duration = settings["video_settings"].get("fade_duration")

            self.show_title = settings["video_settings"]["title"].get("show")
            self.time_title = settings["video_settings"]["title"].get("duration")
            self.title_font_size = settings["video_settings"]["title"].get("font_size")
            self.background_title = tuple(
                map(
                    int,
                    settings["video_settings"]["title"]
                    .get("background_color", "0,0,0")
                    .split(","),
                )
            )
            self.background_title_opacity = settings["video_settings"]["title"].get(
                "background_opacity"
            )
            self.color_title = settings["video_settings"]["title"].get("color")
            self.title_nb_word_per_line = settings["video_settings"]["title"][
                "nb_word_per_line"
            ]

            self.audio_dir = settings["directories"]["audio_dir"]
            self.image_dir = settings["directories"]["image_dir"]
            self.video_dir = settings["directories"]["video_dir"]
            self.music_dir = settings["directories"]["music_dir"]
            self.config_dir = settings["directories"]["config_dir"]

            self.user_data_dir = settings["selenium"]["user_data_dir"]
            self.user_profile_dir_tiktok = settings["selenium"][
                "user_profile_dir_tiktok"
            ]
            self.user_profile_dir_fb = settings["selenium"]["user_profile_dir_fb"]
            self.user_profile_dir_youtube = settings["selenium"][
                "user_profile_dir_youtube"
            ]
            self.fb_asset_id = settings["selenium"]["fb_asset_id"]
            self.fb_business_id = settings["selenium"]["fb_business_id"]
            self.youtube_channel_id = settings["selenium"]["youtube_channel_id"]

            self.aligned_dir = settings["directories"]["aligned_dir"]

            self.csv_path = settings["input_files"]["csv_path"]
            self.is_header_row = settings["input_files"]["is_header_row"]

            self.acoustic_model_path = settings["alignment_model"][
                "acoustic_model_path"
            ]
            self.dict_model_path = settings["alignment_model"]["dict_model_path"]
        except FileNotFoundError:
            print("No config file found. Exiting.")
            sys.exit(1)
        except KeyError as e:
            print(f"Missing key in config file: {e}")
            sys.exit(1)
        except json.decoder.JSONDecodeError:
            print("Invalid config file. Exiting.")
            sys.exit(1)
        except Exception as e:  # pylint: disable=broad-except
            print(f"Unknown error: {e}")
            sys.exit(1)


def generate_save_path(audio1, audio2, extension="mp3"):
    """
    Generates a save path based upon audio filenames.

    Parameters
    ----------
    audio1 : str
        The first audio object.
    audio2 : str
        The second audio object.
    extension : str
        The file extension to use for the output file.

    Returns
    -------
    str
        The save path.
    """
    dir1, filename1_with_ext = os.path.split(audio1.file_path)
    _, filename2_with_ext = os.path.split(audio2.file_path)

    filename1, _ = os.path.splitext(filename1_with_ext)
    filename2, _ = os.path.splitext(filename2_with_ext)

    new_filename = f"{filename1}_{filename2}.{extension}"
    new_path = os.path.join(dir1, new_filename)
    return new_path


class Audio:
    """
    Class for
    """

    def __init__(self, file_path=None, data=None, audio_segment=None):
        if audio_segment is None:
            audio_segment = AudioSegment.from_mp3(os.path.abspath(file_path))
        if data is None:
            data = audio_segment.raw_data
        if file_path is None:
            audio_folder = Config().audio_dir
            file_path = audio_folder + "temp.wav"
            audio_segment.export(file_path, format="wav")
        self.file_path = file_path
        self.data = data
        self.audio_segment = audio_segment

    def get_audio_np_array(self):
        """
        Returns the audio as a numpy array.
        """
        audio = self.audio_segment.set_channels(1)

        return np.array(audio.get_array_of_samples())


def save_wav(audio_bytes, filename, n_channels=1, sample_width=2, frame_rate=44100):
    """
    Save audio bytes to wav file
    """
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(frame_rate)
        wf.writeframes(audio_bytes)
