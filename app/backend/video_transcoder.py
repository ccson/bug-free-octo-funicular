import ffmpeg


class VideoTranscoder(object):

    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id

    def run(self):
        stream = ffmpeg.input(f'{self.tmdb_id}')
        stream = ffmpeg.hflip(stream)
        stream = ffmpeg.output(stream, 'output.h264', **{'-b:v': '1M'})
        ffmpeg.run(stream)
