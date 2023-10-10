"""
path: src/media.py

"""
from moviepy import Clip

from utils import Config


class Media:
    """
    class
    """

    def __init__(self, path: str, media_duration, clip: Clip = None):
        self.path = path
        config = Config()
        self.final_clip_frame_size = config.frame_size
        self.fps = config.fps
        self.clip = clip
        if clip is None:
            self._load_media()
        self._process_from_name(media_duration)

    def _load_media(self):
        """
        Loads the media from the path.
        """

        pass

    def _process_from_name(self, media_duration):
        pass
