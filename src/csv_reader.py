"""
path: src/csv_reader.py

A module that reads a CSV file and populates a list of VideoEntry objects.

Classes:
--------
VideoEntry:
    A class that represents a video entry.

CSVReader:
    A class that reads a CSV file and populates a list of VideoEntry objects.

Functions:
----------
None

Exceptions:
-----------
None

Notes:
------
None

Todo:
-----
None

Author(s):
----------
@concaption
"""

import csv
from utils import Config


class VideoEntry:
    """
    A class that represents a video entry.
    """

    def __init__(self, script, title, hashtags, description, filename=None):
        self.script = script
        self.title = title
        self.hashtags = hashtags
        self.description = description
        self.filename = filename


class CSVReader:
    """
    A class that reads a CSV file and populates a list of VideoEntry objects.

    Attributes:
    -----------
    file_path : str
        The path to the CSV file to be read.
    is_header_row : bool
        A flag indicating whether the CSV file has a header row.
    video_entries : list
        A list of VideoEntry objects populated from the CSV file.

    Methods:
    --------
    __init__(self, csv_path=None):
        Initializes a CSVReader object with the given CSV file path.
        If no path is provided,the default path from the
        Config object is used.
        Reads the CSV file and populates the video_entries
        attribute with VideoEntry objects.

    read_csv(self):
        Reads the CSV file and populates the video_entries attribute with VideoEntry objects.

    get_video_entries(self):
        Returns the list of VideoEntry objects.
    """

    def __init__(self, csv_path=None):
        config = Config()  # instantiate config to get settings
        self.file_path = csv_path if csv_path else config.csv_path
        self.is_header_row = config.is_header_row
        self.video_entries = []
        self.read_csv()

    def read_csv(self):
        """
        Reads a CSV file and populates the video_entries attribute with VideoEntry objects.
        """
        try:
            with open(self.file_path, mode='r', encoding='utf') as file:
                csv_read = csv.reader(file)
                if self.is_header_row:
                    next(csv_read)
                for row in csv_read:
                    if len(row) == 4:
                        filename = None
                        script, video_title, hashtags, video_description = row
                    elif len(row) == 5:
                        filename, script, video_title, hashtags, video_description = row

                    video_entry = VideoEntry(
                        script, video_title, hashtags, video_description, filename)
                    self.video_entries.append(video_entry)

        except FileNotFoundError:
            print(f'File not found: {self.file_path}')
        except Exception as e:  # pylint: disable=broad-except
            print(f'An error occurred while reading the file: {e}')

    def get_video_entries(self):
        """
        Returns a list of VideoEntry objects.
        """
        return self.video_entries


if __name__ == '__main__':
    csv_reader = CSVReader()
    video_entries = csv_reader.get_video_entries()
    for entry in video_entries:
        print("""
              Script: {entry.script}, 
              Title: {entry.title}, 
              Hashtags: {entry.hashtags}, 
              Description: {entry.description}, 
              Filename: {entry.filename}
              """)
