import ffmpeg
import os
import pathlib

from datetime import datetime


class VideoTranscoder(object):

    INPUT_FOLDER = os.getenv('UPLOADS_FOLDER')
    OUTPUT_FOLDER = os.getenv('COMPLETE_FOLDER')
    OUTPUT_CODEC = 'h264'
    VIDEO_BITRATE = '1000'

    def __init__(self, imdb_id, file_extension):
        self.imdb_id = imdb_id
        self.file_extension = file_extension
        self.input_file_name = f'{self.imdb_id}.{self.file_extension}'
        self.input_file_full_path = os.path.join(VideoTranscoder.INPUT_FOLDER, self.input_file_name)
        self.input_file_pathlib = pathlib.Path(self.input_file_full_path)
        self.input_file_size = self.input_file_pathlib.stat().st_size

        self.output_file_full_path = os.path.join(
            VideoTranscoder.OUTPUT_FOLDER, f'{self.imdb_id}.{VideoTranscoder.OUTPUT_CODEC}'
        )
        self.output_file_pathlib = pathlib.Path(self.output_file_full_path)

    def run(self):
        stream = ffmpeg.input(self.input_file_full_path)
        stream = ffmpeg.hflip(stream)
        stream = ffmpeg.output(stream, self.output_file_full_path, **{
            'f': self.file_extension,
            'vcodec': VideoTranscoder.OUTPUT_CODEC,
            'video_bitrate': VideoTranscoder.VIDEO_BITRATE
        })
        ffmpeg.run(stream, overwrite_output=True)

    def get_transcode_timestamp(self):
        self._check_output_file_exists()
        return datetime.fromtimestamp(self.output_file_pathlib.stat().st_mtime)

    def get_output_file_size(self):
        self._check_output_file_exists()
        return self.output_file_pathlib.stat().st_size

    def get_input_file_size(self):
        return self.input_file_size

    def _check_output_file_exists(self):
        if not self.output_file_pathlib.exists():
            raise FileNotFoundError(f'File ({self.output_file_pathlib.name}) Not Found')
